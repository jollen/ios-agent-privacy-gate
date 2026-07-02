# iOS Agent Privacy Gate

`ios-agent-privacy-gate` 是一個可重用的 ChatGPT Skill，用於審查 iOS App 導入 AI、LLM 或 Agentic AI 功能時的安全性、隱私邊界、使用者確認流程與 App Store 審查風險。

## 這個 Skill 用來做什麼

當 iOS 專案新增或修改以下功能時，適合使用本 Skill：

- AI 摘要、分類、標籤或建議
- Agentic AI 工作流或多步驟 AI 動作
- 將 OCR、語音、照片、文件、筆記內容送交 AI 模型
- 從 App 匯出 prompt/context/observation context
- 使用 OpenAI、Claude、Gemini 或自訂 LLM endpoint 等外部 AI 服務
- AI 產生草稿、檢查清單、報告、回覆或後續建議
- 與 AI 相關的 Settings、隱私政策、App Store metadata 或 release copy 文案

核心原則是：

> Security & Privacy 優先。AI 輸出預設只是草稿，除非使用者明確確認，否則不得自動執行動作。

## 主要審查 Gate

本 Skill 會用以下 Gate 審查 AI 功能：

1. **Feature boundary** — 定義 AI 功能的範圍、輸入、輸出與副作用。
2. **Data boundary** — 分類資料類型、是否離開裝置、是否需要 redaction。
3. **Agent action boundary** — 判斷 AI 可以建議什麼、什麼需要使用者確認、什麼必須阻擋。
4. **Local-first alternative** — 優先評估 iOS SDK、規則引擎、on-device processing，而不是直接使用外部 AI。
5. **UX and Settings disclosure** — 讓使用者清楚知道 AI 是否啟用、使用哪些資料、是否可關閉。
6. **App Store and release copy review** — 檢查 `Info.plist`、`PrivacyInfo.xcprivacy`、App Store metadata、審查備註、Privacy / Terms 與 release copy 文案。
7. **Repository scan** — 使用內建腳本加速靜態檢查。

## 內建掃描腳本

本 Skill 內含：

```bash
scripts/scan_ios_ai_privacy.py
```

使用範例：

```bash
python3 scripts/scan_ios_ai_privacy.py /path/to/ios/project --json
```

此腳本會掃描常見 AI / Privacy 指標，例如外部 AI 關鍵字、prompt/context 用語、可能的敏感資料類型、權限檔案、Settings 畫面，以及可能造成副作用的動作字詞。掃描結果只是 checklist accelerator，不能取代人工產品與安全審查。

## 建議輸出格式

典型審查結果應包含：

- AI Feature Summary
- Data Boundary Review
- Agent Action Boundary Review
- Local-first Alternative Review
- UX and Settings Requirements
- App Store / PrivacyInfo / Release Copy Review
- Required Changes
- Final Decision: Pass、Needs Work 或 Blocked

## 設計原則

- 預設 local-first。
- 外部傳輸採 default deny，除非有明確且使用者可理解的理由。
- 送交外部 AI 前，優先進行 redaction。
- 外部 AI 輸出預設只視為草稿。
- 儲存、刪除、送出、分享、上傳、同步、付款、排程或修改 source-of-truth data 前，必須取得使用者確認。
- 外部 AI 關閉時，App 仍應可用。
- Production UI 文案避免使用「prompt」「agent pipeline」等工程語氣。

## 與 iOS production workflow 的關係

本 Skill 是一般 iOS production pipeline 的補充，而不是取代。Production pipeline 負責 App 架構、Roadmap、Build 檢查、UI、Performance、Packaging 與 Release readiness。本 Skill 專門用於 AI、LLM、Privacy、Context export、Agent action 或外部模型呼叫進入產品設計時的安全審查。
