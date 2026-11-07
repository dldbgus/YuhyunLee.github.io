# Yuhyun Lee 연구자 홈페이지 — 시작하기

## 먼저, 이 홈페이지는 어떻게 작동하나요?

- **GitHub Pages:** 실제 공개 홈페이지. 무료로 호스팅할 수 있습니다.
- **Pages CMS:** 글과 이미지를 수정하는 편집 화면. 별도 코딩이 필요 없습니다.
- **자동 게시:** Pages CMS에서 Save하면 GitHub에 저장되고, GitHub Actions가 새 사이트를 만들어 게시합니다.
- **디자인:** `styles.css`는 그대로 유지되므로 글이나 이미지를 바꿔도 디자인이 유지됩니다.
- **프로젝트 상세 페이지:** 연구 프로젝트마다 독립 페이지가 자동 생성됩니다.

> 아직 온라인에 게시된 사이트는 아닙니다. 본인 GitHub 계정에서 공개 및 Pages CMS 연결이 필요합니다.

## 1. GitHub Pages에서 공개하기 (최초 1회)

1. [GitHub](https://github.com/) 로그인 → 오른쪽 위 `+` → **New repository**.
2. 저장소 이름을 **`YOUR_GITHUB_USERNAME.github.io`**로 지정합니다. 예: 사용자 이름이 `yuhyunlee`라면 `yuhyunlee.github.io`입니다. 실제 사용자의 GitHub ID와 정확히 일치해야 합니다.
3. **Public** 선택 → **Create repository**.
4. 이 ZIP의 내용 전체(압축 해제 후 모든 파일)를 저장소 루트에 업로드합니다. 숨김 파일인 **`.pages.yml`**, **`.github/workflows/publish.yml`**도 반드시 포함하세요. ZIP 자체를 업로드하는 것이 아닙니다.
   - GitHub의 `Add file` → `Upload files`를 이용할 수 있습니다. 브라우저가 숨김 파일을 무시하면 GitHub 웹 에디터나 Git 명령으로 추가해야 합니다.
5. `Settings` → `Pages` → `Build and deployment` → **Source: GitHub Actions**로 설정합니다.
6. `Actions` 탭 → `Publish research portfolio` 워크플로가 성공했는지 확인합니다. 처음에는 `Run workflow`를 직접 눌러도 됩니다.
7. 최종 주소: **`https://YOUR_GITHUB_USERNAME.github.io/`**

**중요:** `Deploy from a branch`가 아니라 **GitHub Actions**를 사용해야 수정 사항이 자동 반영됩니다.

## 2. 코딩 없이 글·그림 편집하기 (최초 1회)

1. [Pages CMS](https://app.pagescms.org/) 접속 → **Sign in with GitHub**.
2. Pages CMS에서 **GitHub App 접근 승인/설치**가 필요하면, 자신의 계정과 방금 만든 저장소만 선택해 권한을 부여합니다.
3. CMS의 저장소 목록에서 `YOUR_GITHUB_USERNAME.github.io`, 브랜치 `main`을 엽니다.
4. 왼쪽 편집 메뉴가 보입니다:

| 메뉴 | 편집할 수 있는 것 |
|------|-----------------|
| `01 · Homepage & contact` | 이름, 소개, 구직 여부, 프로필 사진, 이메일, CV, LinkedIn 등 |
| `02 · Research projects` | 프로젝트 추가/삭제/순서 변경, 본인 기여, 결과, 대표 이미지, 여러 Figure |
| `03 · Publications` | 논문 추가/삭제, 저자, DOI 링크 |
| `04 · Skills & expertise` | 능력, 기술, 툴, 키워드 |
| `05 · Education` | 학력 및 지도교수 |
| `06 · Awards & recognition` | 수상, 특허, 연구 하이라이트 |

5. 수정한 뒤 **Save**합니다. GitHub `Actions`에서 게시 작업이 성공하면 웹사이트에 반영됩니다. 즉각적인 실시간 편집 미리보기는 아니며, 빌드/배포 단계를 거칩니다.

## 3. 실험 사진과 논문 Figure 넣기

1. Pages CMS → `02 · Research projects` → 원하는 프로젝트를 엽니다.
2. `Main project image`에서 사진/그림을 업로드합니다. 기존 콘셉트 그래픽을 해당 이미지로 대체합니다.
3. `Additional figure gallery`에 여러 이미지를 업로드할 수 있습니다. 그러면 해당 **개별 프로젝트 페이지**에 Figure 갤러리가 생깁니다.
4. `Main image caption / disclaimer`에 반드시 그림을 설명하세요. 업로드 전에 다른 저자의 그림이나 미출판 데이터의 공개 허가를 확인하세요.
5. **Save**하면 됩니다. 이미지 이름/업로드된 경로는 CMS가 관리합니다.

권장 이미지: JPG, PNG 또는 WebP. 1400–2000px 정도의 이미지를 우선 권장하며 파일이 너무 커지지 않도록 압축하세요.

## 4. 새 연구 프로젝트 추가하기

1. `02 · Research projects`에서 **Add item**을 눌러 프로젝트를 만듭니다.
2. `URL slug`: 영문 소문자·숫자·하이픈만, 기존 프로젝트와 중복되지 않게 입력하세요. 예: `adaptive-brain-stimulation`.
3. `Short overview`, `My contribution`, `Findings and significance`를 입력합니다. 무엇을 했는지와 무엇을 실제로 보였는지를 구분하세요.
4. 대표 이미지를 추가하거나 `Fallback artwork`를 선택하세요.
5. 저장하면 새 카드가 홈페이지에 생성되고 `/projects/adaptive-brain-stimulation/` 상세 페이지도 자동으로 생성됩니다.

## 5. 이력서 업데이트

`Homepage & contact` → `CV PDF`에서 최신 PDF를 선택/업로드합니다. 기존 CV는 2026년 10월 버전이므로 **공개 전에 최신화**하는 것을 추천합니다. 페이지의 다운로드 버튼이 자동으로 최신 업로드 PDF를 가리킵니다.

## 6. 사전 점검

- 최신 학위 일정 및 구직 상태
- 이름, 이메일, Google Scholar/LinkedIn 링크, CV
- 논문 출판 정보 및 DOI가 정확한지
- 논문 Figure, 조직 로고, 동물·환자 이미지 공개 권한
- 미출판 연구 데이터와 내부 기밀 내용 공개 여부
- 프로젝트별 연구 결과에 대한 주장 수준: selectivity 등은 검증되지 않았으면 단정하지 않기

## 7. 로컬에서 보고 싶다면 (선택)

ZIP 압축을 풀고 `index.html`을 더블클릭하면 초기 홈페이지를 볼 수 있습니다. 내용(`data/*.json`)을 직접 바꿨다면 컴퓨터에 Python이 설치된 경우:

```bash
python3 scripts/build.py
```

실행 후 `index.html`을 다시 열면 변경 사항을 확인할 수 있습니다. 그러나 **일상적인 수정은 로컬 파일이 아니라 Pages CMS에서 진행하면 됩니다.**

## 문제 해결

- **CMS에 저장소가 보이지 않아요** → Pages CMS GitHub App이 해당 저장소에 접근할 수 있도록 승인했는지 확인합니다.
- **글을 수정했는데 라이브 사이트가 그대로예요** → GitHub `Actions` 탭의 `Publish research portfolio` 상태와 `Settings → Pages → Source: GitHub Actions`를 확인합니다.
- **이미지가 깨져요** → Pages CMS의 media 경로(`/assets/uploads`)를 통해 업로드하세요. GitHub username.github.io 형식의 저장소를 권장합니다.
- **빌드 실패** → 프로젝트 URL slug가 유일하고 `a-z`, `0-9`, `-`만 포함하는지 확인합니다. `Actions`의 에러 메시지를 보면 됩니다.
- **개별 페이지가 404예요** → `Actions`에서 배포가 성공했는지 확인하고 페이지 주소 끝에 `/`를 붙입니다.

공식 안내: [GitHub Pages 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [Pages CMS 시작하기](https://pagescms.org/docs/quick-start/)
