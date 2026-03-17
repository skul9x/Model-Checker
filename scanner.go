package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"regexp"
	"sort"
	"sync"
	"time"
)

type ModelInfo struct {
	Name        string `json:"name"`
	Description string `json:"description"`
}

type KeyResult struct {
	Key    string      `json:"key"`
	Status string      `json:"status"` // "ACTIVE" or "ERROR"
	Models []ModelInfo `json:"models"`
	Error  string      `json:"error"`
}

type APIResponse struct {
	Models []ModelInfo `json:"models"`
	Error  *struct {
		Message string `json:"message"`
	} `json:"error"`
}

type TestRequest struct {
	Contents []struct {
		Parts []struct {
			Text string `json:"text"`
		} `json:"parts"`
	} `json:"contents"`
}

type TestResponse struct {
	Candidates []struct {
		Content struct {
			Parts []struct {
				Text string `json:"text"`
			} `json:"parts"`
		} `json:"content"`
	} `json:"candidates"`
	Error *struct {
		Message string `json:"message"`
	} `json:"error"`
}

func ExtractAPIKeys(text string) []string {
	pattern := `AIza[0-9A-Za-z\-_]{35}`
	re := regexp.MustCompile(pattern)
	matches := re.FindAllString(text, -1)

	keyMap := make(map[string]bool)
	for _, k := range matches {
		keyMap[k] = true
	}

	uniqueKeys := make([]string, 0, len(keyMap))
	for k := range keyMap {
		uniqueKeys = append(uniqueKeys, k)
	}
	sort.Strings(uniqueKeys)
	return uniqueKeys
}

func CheckSingleKey(apiKey string) KeyResult {
	url := fmt.Sprintf("https://generativelanguage.googleapis.com/v1beta/models?key=%s", apiKey)
	
	client := &http.Client{
		Timeout: 10 * time.Second,
	}

	resp, err := client.Get(url)
	if err != nil {
		return KeyResult{
			Key:    apiKey,
			Status: "ERROR",
			Error:  "Lỗi kết nối mạng: " + err.Error(),
		}
	}
	defer resp.Body.Close()

	var apiResp APIResponse
	if err := json.NewDecoder(resp.Body).Decode(&apiResp); err != nil {
		return KeyResult{
			Key:    apiKey,
			Status: "ERROR",
			Error:  "Lỗi phân giải dữ liệu: " + err.Error(),
		}
	}

	if apiResp.Error != nil {
		return KeyResult{
			Key:    apiKey,
			Status: "ERROR",
			Error:  "Yêu cầu không hợp lệ hoặc Key sai",
		}
	}

	if resp.StatusCode != http.StatusOK {
		return KeyResult{
			Key:    apiKey,
			Status: "ERROR",
			Error:  fmt.Sprintf("Mã lỗi HTTP %d", resp.StatusCode),
		}
	}

	models := apiResp.Models
	for i := range models {
		if models[i].Description == "No description available" {
			models[i].Description = "Không có mô tả cho model này"
		}
	}

	return KeyResult{
		Key:    apiKey,
		Status: "ACTIVE",
		Models: models,
	}
}

func (a *App) ScanKeys(text string) []KeyResult {
	keys := ExtractAPIKeys(text)
	var wg sync.WaitGroup
	results := make([]KeyResult, len(keys))

	for i, key := range keys {
		wg.Add(1)
		go func(idx int, k string) {
			defer wg.Done()
			results[idx] = CheckSingleKey(k)
		}(i, key)
	}

	wg.Wait()
	return results
}

func (a *App) TestModel(apiKey string, modelName string) (string, error) {
	url := fmt.Sprintf("https://generativelanguage.googleapis.com/v1beta/%s:generateContent?key=%s", modelName, apiKey)
	
	reqBody := TestRequest{
		Contents: []struct {
			Parts []struct {
				Text string `json:"text"`
			} `json:"parts"`
		}{
			{
				Parts: []struct {
					Text string `json:"text"`
				}{ {Text: "hi"} },
			},
		},
	}

	jsonData, _ := json.Marshal(reqBody)
	
	client := &http.Client{Timeout: 15 * time.Second}
	resp, err := client.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("lỗi kết nối: %v", err)
	}
	defer resp.Body.Close()

	var testResp TestResponse
	if err := json.NewDecoder(resp.Body).Decode(&testResp); err != nil {
		return "", fmt.Errorf("lỗi đọc dữ liệu: %v", err)
	}

	if testResp.Error != nil {
		return "", fmt.Errorf("lỗi API: %s", testResp.Error.Message)
	}

	if len(testResp.Candidates) > 0 && len(testResp.Candidates[0].Content.Parts) > 0 {
		return testResp.Candidates[0].Content.Parts[0].Text, nil
	}

	return "", fmt.Errorf("model không trả về nội dung (Mã: %d)", resp.StatusCode)
}
