# Diff-Update-Request-Generator-CN

📖[English README.md](#Diff-Update-Request-Generator-EN)📖

## 這是一個簡單的工具，用於生成特定文件的Update Requirements。

## How to use
- 下載 [最新Release](https://github.com/KXX-GSS/Diff_Update_Request_Generator/releases)。
- 填寫Config案所需的資訊。
- 執行 Diff-Update-Request-Generator.exe 生成新的 Update Requests。

### 系統要求
- Python 3.6 或更新版本

## 關於 Config 
```

path_to_initial_file : ''

path_to_update_file : ''

diff_file_directory : ''

diff_update_request_name : ''
```
| 變數名稱                      | 是否必填 | 預設值                                   | 描述                                                         |
|------------------------------|----------|---------------------------------------|------------------------------------------------------------|
| path_to_initial_file         | 是       | 無。                                   | 初始文件的目錄路徑。                                         |
| path_to_update_file          | 是       | 無。                                   | 更新文件的目錄路徑。                                         |
| diff_file_directory          | 否       | 腳本的當前目錄。                        | diff_update_request的目錄路徑。                                     |
| diff_update_request_name     | 否       | 'diff_update_request.txt'。            | diff_update_request檔案的名稱。                                         |
| diff_update_request_project_name     | 否       | 'diff_update_request_{date}'。            | diff project名稱。                                         |

## 貢獻專案

### 如何貢獻

1. Fork 此專案。
2. 將您 Fork 的專案克隆到您的本地機器。
3. 創建一個新的分支。
4. 貢獻您的代碼。
5. 提交/推送您的代碼。
6. 創建一個新的 Pull Request。
7. 等待回應。

### 代碼編寫/提交指南

* 保持每行代碼在 100 個字元以內。
* 變數和函數名稱使用 `snake_case` 命名方式。
* 在檔案末尾添加一個空白行。
* 優化代碼並移除不必要的導入。
* 使用以下格式撰寫提交訊息，並用英文書寫：
  * Update - 在此處寫入您的提交訊息
  * Fix bug - 在此處寫入您的提交訊息
  * Optimize - 在此處寫入您的提交訊息
  * Standardize - 在此處寫入您的提交訊息

### 建議/問題回報

如果您有任何建議或發現任何問題，請在 [Issue](https://github.com/KXX-GSS/Diff_Update_Request_Generator/issues) 提交您的反饋，我會盡快回應！

# Diff-Update-Request-Generator-EN

📖[繁體中文版 README.md](#Diff-Update-Request-Generator-CN)📖

## This is a simple tool to generate a diff update request for a given file.

## How to use
- download the [latest release](https://github.com/KXX-GSS/Diff_Update_Request_Generator/releases)  .
- Fill the config file with the required information.
- Run Diff-Update-Request-Generator.exe to generate the Update Requests.

## About the Config File
```

path_to_initial_file : ''

path_to_update_file : ''

diff_file_directory : ''

diff_update_request_name : ''
```
| Variable Name           | Default Value                         | Description                                            |
|-------------------------|---------------------------------------|--------------------------------------------------------|
| path_to_initial_file    | The current directory of the script.  | The directory path of the initial file.                |
| path_to_update_file     | The current directory of the script.  | The directory path of the update file.                 |
| diff_file_directory     | The current directory of the script.  | The directory path of the diff update request.         |
| diff_update_request_name | The current date, followed by '_diff_update_request'. | The name of the diff update request.                   |

## Contributing to the Project

### How to Contribute

1. Fork this project.
2. Clone your forked project to your local machine.
3. Create a new branch.
4. Contribute your code.
5. Commit/Push your code.
6. Create a new Pull Request.
7. Wait for a response.

### Code Writing/Commit Guidelines

* Keep each line under 100 characters.
* Use `snake_case` for variable and function names.
* Add a trailing blank line at the end of files.
* Optimize code and remove unnecessary imports.
* Use the following format for commit messages and write them in English:
  * Update - your commit messages here
  * Fix bug - your commit messages here
  * Optimize - your commit messages here
  * Standardize - your commit messages here

### Suggestions/Issue Reporting

If you have any suggestions or discover any issues, please submit your feedback in the [Issues](https://github.com/KXX-GSS/Diff_Update_Request_Generator/issues) section, and I will respond as soon as possible!
