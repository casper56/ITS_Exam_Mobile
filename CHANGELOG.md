# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-02-05

### 🚀 Major Refactoring & Cleanup
- **Directory Structure**:
  - Migrated all exam content (`AI900`, `ITS_Python`, etc.) from root to `www/` directory.
  - Removed redundant root-level folders to ensure a clean Web App structure.
  - Removed `android_sdk_copy` to free up disk space.
- **Config Restoration**:
  - Restored missing `package.json` and `capacitor.config.json`.

### 📚 Content Updates
- **ITS Python**:
  - Fixed Q14 formatting (newline issue).
  - Added **10 Guess Questions** (Q89-Q98) covering advanced topics (slicing, scope, etc.).
  - Added **10 Syllabus-Aligned Questions** (Q109-Q118) covering missing objectives (f-strings, pydoc, random.sample, io.StringIO, etc.).
  - **Total**: 118 Questions.
- **ITS AI**:
  - Added **10 Supplement Questions** (Q99-Q108) covering Anomaly Detection, Semantic Segmentation, NER, and Responsible AI.
  - Marked new questions with `【補充】` tag.
  - **Total**: 108 Questions.

### 🛠️ Feature & Bug Fixes
- **PDF Generation**:
  - Fixed `json_to_pdf.py` hardcoded path issue.
  - Standardized PDF filenames to match JSON (e.g., `questions_ITS_python.pdf`).
  - Regenerated all 6 category PDFs with full content.
- **Web App**:
  - Implemented `localStorage` logic to **save user answers** across page reloads.
  - Synced all HTML files with the latest JSON data.

### 🤖 CI/CD & Automation
- **GitHub Actions**:
  - Created `.github/workflows/build_apk.yml` for automated Android APK building.
  - Upgraded `upload-artifact` to v4 to resolve deprecation warnings.
  - Enabled automatic builds on push to `main` and `dev` branches.

### 📖 Documentation
- Added `git_commit.md`: A guide for Git operations and workflow.
- Updated `BUILD_APK.md`: Revised instructions to recommend GitHub Actions cloud build.
