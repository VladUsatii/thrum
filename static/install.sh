#!/usr/bin/env bash
set -euo pipefail

thrum_logo() {
cat <<'EOF'
                                                                        
                  ░                                                     
      ▒           ▓░                                                    
      ▒           ▓░                                                    
      ▒           ▓░                                                    
      ▒           ▓░                                                    
      ▒           ▓░                                                    
      ▒           ▓░                                                    
   ▓▓▓█▓▓▒▒▒      ▓░                                                    
      ▒           ▓░░▓▒▓                    ▒▒       ░▓▓    ▒▓░         
      ▒           ▓▓░  ▒▒   ░▒ ░▒▓░    ▓    ▓▒    ▒░▓░ ░▓░▓░  ▓░        
      ░░          █▒   ░▓   ░▓▓        ▓   ░▒▓    ▒▒    ▓█     ▓        
      ░▓         ░█░    ▓   ░▓         ▓  ░▓░▓░   ▓     ░▒     ▓░       
       ░▓        ░▒     ▓   ░▒         ▓ ░▓░ ░▓   ▒     ░▒     ▓░       
        ░▓       ░▒     ▓   ░▓         ▓▒▓░   ▒▒  ░     ░░     ░░       
         ░▒▓░           ▒░  ░▓                                          
                             ▓░                                         
                                                                        
EOF
}

echo "[thrum] Installing thrum CLI from source..."
echo
thrum_logo
echo

# ---- config ----
REPO_URL="https://github.com/vladusatii/getthrum.git"
BINARY_NAME="thrum"
DEST_DIR="${HOME}/.local/bin"

# ---- checks ----
if ! command -v git >/dev/null 2>&1; then
  echo "[thrum] error: git is not installed (needed to fetch source)" >&2
  exit 1
fi

if ! command -v go >/dev/null 2>&1; then
  echo "[thrum] error: Go is not installed (needed to build CLI)" >&2
  exit 1
fi

mkdir -p "${DEST_DIR}"

# ---- clone + build ----
TMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t thrum-install)"
echo "[thrum] using temp dir: ${TMP_DIR}"

git clone --depth=1 "${REPO_URL}" "${TMP_DIR}"
cd "${TMP_DIR}"

echo "[thrum] running: go build -o ${BINARY_NAME} ."
go build -o "${BINARY_NAME}" .

mv "${BINARY_NAME}" "${DEST_DIR}/${BINARY_NAME}"

echo
echo "[thrum] Installed ${BINARY_NAME} to ${DEST_DIR}/${BINARY_NAME}"
echo "[thrum] Make sure ${DEST_DIR} is in your \$PATH. Then you can run:"
echo
echo "   thrum --version"
echo

cd /
rm -rf "${TMP_DIR}" || true