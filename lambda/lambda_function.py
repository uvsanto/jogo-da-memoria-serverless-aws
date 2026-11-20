#!/usr/bin/env bash
# Publica as evidências e os arquivos do projeto no repositório e corrige o README.
# Uso (Git Bash no Windows, Linux ou macOS):  bash publicar-evidencias.sh
set -euo pipefail

# ====== AJUSTE AQUI ======
REPO_URL="https://github.com/uvsanto/jogo-da-memoria-serverless-aws.git"
IMG_DIR="$HOME/Downloads/prints"          # pasta com os prints originais
PROJ_DIR="$HOME/Downloads/memory-game"    # pasta do jogo (index.html, css/, js/, assets/)
LAMBDA_FILE="$HOME/Downloads/lambda_function.py"  # código final da Lambda
WORK_DIR="$HOME/jogo-da-memoria-serverless-aws"   # onde o repositório será clonado
# ==========================

# nome original  ->  novo nome (sem espaços, minúsculo)
declare -A MAPA=(
  ["DynamoDB- Pint 1.png"]="dynamodb-itens.png"
  ["Teste Lambda 02.png"]="lambda-teste.png"
  ["API Gateway_02.png"]="api-gateway-recursos.png"
  ["memory-game-lab-vagner-santos_final.png"]="s3-bucket.png"
)

[ -d "$WORK_DIR/.git" ] || git clone "$REPO_URL" "$WORK_DIR"
cd "$WORK_DIR"
git pull --ff-only
mkdir -p Docs lambda

echo ">> Copiando prints com os novos nomes"
for antigo in "${!MAPA[@]}"; do
  novo="${MAPA[$antigo]}"
  if [ -f "$IMG_DIR/$antigo" ]; then
    cp "$IMG_DIR/$antigo" "Docs/$novo"; echo "   OK   $antigo -> Docs/$novo"
  else
    echo "   FALTA $IMG_DIR/$antigo (confira o nome/extensão)"
  fi
done

echo ">> Copiando arquivos do projeto"
for item in index.html css js assets; do
  if [ -e "$PROJ_DIR/$item" ]; then cp -r "$PROJ_DIR/$item" .; echo "   OK   $item"
  else echo "   FALTA $PROJ_DIR/$item"; fi
done
[ -f "$LAMBDA_FILE" ] && cp "$LAMBDA_FILE" lambda/lambda_function.py && echo "   OK   lambda/lambda_function.py"

echo ">> Atualizando a seção de evidências do README"
cat > /tmp/evidencias.md <<'MD'
## 📸 Evidências da Implantação

### Tabela NoSQL (Amazon DynamoDB)
![Tabela DynamoDB com os itens das partidas](Docs/dynamodb-itens.png)

### Backend Serverless (AWS Lambda)
![Teste da função Lambda com resposta 200](Docs/lambda-teste.png)

### Endpoints REST (Amazon API Gateway)
![Recursos e métodos da API REST](Docs/api-gateway-recursos.png)

### Hospedagem Estática (Amazon S3)
![Bucket S3 com os arquivos do jogo](Docs/s3-bucket.png)

MD
awk '
  /^## .*Evidências da Implantação/ { while ((getline l < "/tmp/evidencias.md") > 0) print l; skip=1; next }
  skip && /^---[[:space:]]*$/ { skip=0 }
  !skip { print }
' README.md > README.novo && mv README.novo README.md

git add -A
git status --short
if git diff --cached --quiet; then echo "Nada para commitar."; exit 0; fi
git commit -m "Adiciona evidências, arquivos do projeto e corrige links do README"
git push origin main
echo "Pronto! Abra o repositório no GitHub e confira as imagens."