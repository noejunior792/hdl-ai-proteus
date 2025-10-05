# HDL AI Proteus - Quick Commands Reference

Este arquivo contém todos os comandos essenciais para usar o HDL AI Proteus.

## 🚀 Início Rápido

### Primeira vez (setup completo)
```bash
# Clone o repositório
git clone https://github.com/noejunior792/hdl-ai-proteus.git
cd hdl-ai-proteus

# Setup automático
make quick-start

# Ou manualmente:
make install-system    # Instala dependências do sistema
make setup-env         # Cria diretórios e .env
make install           # Instala dependências Python
```

### Executar a API
```bash
# Método 1: Script de inicialização (Recomendado)
python3 run.py

# Método 2: Make commands
make run              # Modo normal
make run-dev          # Modo desenvolvimento (debug)
make run-prod         # Modo produção (Gunicorn)

# Método 3: Direto
python3 src/app.py
```

## 🐳 Docker

### Build e execução
```bash
# Build da imagem
make docker-build
# ou
docker build -t hdl-ai-proteus .

# Executar container
make docker-run
# ou
docker run -d --name hdl-api -p 5000:5000 hdl-ai-proteus

# Docker Compose (Recomendado para produção)
docker-compose up -d
```

### Gerenciamento Docker
```bash
# Ver logs
make docker-logs
docker logs -f hdl-api

# Parar
make docker-stop
docker-compose down
```

## 🔧 Desenvolvimento

### Setup ambiente de desenvolvimento
```bash
make dev-setup        # Setup completo para desenvolvimento
make install-dev      # Instala ferramentas de desenvolvimento
```

### Ferramentas de qualidade
```bash
make lint            # Verificar código
make format          # Formatar código
make check-deps      # Verificar dependências
make clean           # Limpar arquivos temporários
```

## 📡 Testando a API

### Health check
```bash
# Via make
make health

# Via curl
curl http://localhost:5000/health

# Resposta esperada:
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "service": "HDL AI Proteus",
  "version": "1.0.0"
}
```

### Listar provedores disponíveis
```bash
curl http://localhost:5000/api/providers
```

### Testar conexão com provedor
```bash
curl -X POST http://localhost:5000/test-provider \
  -H "Content-Type: application/json" \
  -d '{
    "provider_config": {
      "provider_type": "azure_openai",
      "api_key": "sua-chave-api",
      "endpoint": "https://seu-recurso.openai.azure.com/",
      "api_version": "2024-02-15-preview"
    }
  }'
```

### Gerar projeto HDL
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 4-bit counter in VHDL with enable and reset",
    "circuit_name": "counter_4bit",
    "provider_config": {
      "provider_type": "azure_openai",
      "api_key": "sua-chave-api",
      "endpoint": "https://seu-recurso.openai.azure.com/",
      "api_version": "2024-02-15-preview"
    }
  }' \
  --output counter_4bit.pdsprj
```

## ⚙️ Configuração

### Variáveis de ambiente principais
```bash
# Servidor
export SERVER_HOST=0.0.0.0
export SERVER_PORT=5000
export SERVER_DEBUG=false

# Aplicação
export DEFAULT_PROVIDER=azure_openai
export LOG_LEVEL=INFO

# Compiladores (se não estiverem no PATH)
export GHDL_PATH=/caminho/para/ghdl
export IVERILOG_PATH=/caminho/para/iverilog
```

### Criar arquivo .env
```bash
# Copiar template
cp env.template .env

# Editar com suas configurações
nano .env
```

## 🔍 Debug e Logs

### Ver logs
```bash
# Logs da aplicação
make logs
tail -f logs/hdl_proteus.log

# Logs do Docker
make docker-logs
```

### Modo debug
```bash
# Local
export LOG_LEVEL=DEBUG
python3 run.py

# Docker
docker run -e LOG_LEVEL=DEBUG hdl-ai-proteus
```

## 🛠️ Troubleshooting

### Problemas comuns e soluções
```bash
# 1. Dependências em falta
make check-deps
make install-system

# 2. GHDL não encontrado
sudo apt install ghdl
# ou
export GHDL_PATH=/caminho/para/ghdl

# 3. Icarus Verilog não encontrado
sudo apt install iverilog
# ou
export IVERILOG_PATH=/caminho/para/iverilog

# 4. Porta em uso
export SERVER_PORT=8000

# 5. Permissões de arquivo
sudo chown -R $USER:$USER .
chmod +x run.py
```

## 📝 Exemplos de Uso

### Python
```python
import requests

data = {
    "prompt": "Create a simple AND gate in VHDL",
    "circuit_name": "and_gate",
    "provider_config": {
        "provider_type": "azure_openai",
        "api_key": "sua-chave",
        "endpoint": "https://seu-recurso.openai.azure.com/",
        "api_version": "2024-02-15-preview"
    }
}

response = requests.post("http://localhost:5000/generate", json=data)
if response.status_code == 200:
    with open("and_gate.pdsprj", "wb") as f:
        f.write(response.content)
```

### JavaScript
```javascript
const response = await fetch('http://localhost:5000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Create a simple AND gate in VHDL',
    circuit_name: 'and_gate',
    provider_config: {
      provider_type: 'azure_openai',
      api_key: 'sua-chave',
      endpoint: 'https://seu-recurso.openai.azure.com/',
      api_version: '2024-02-15-preview'
    }
  })
});

const blob = await response.blob();
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'and_gate.pdsprj';
a.click();
```

## 🤝 Contribuindo

### Setup para contribuição
```bash
# Fork e clone seu fork
git clone https://github.com/seu-usuario/hdl-ai-proteus.git
cd hdl-ai-proteus

# Setup ambiente
make dev-setup

# Criar branch
git checkout -b feature/nova-funcionalidade

# Fazer alterações e testar
make lint
make format
make run-dev

# Commit e push
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nova-funcionalidade
```

### Adicionar novo provedor AI
1. Criar arquivo em `src/providers/seu_provedor.py`
2. Herdar de `BaseAIProvider`
3. Implementar métodos obrigatórios
4. Registrar em `provider_factory.py`
5. Atualizar documentação em `docs/api_context.json`

## 📞 Ajuda

### Documentação
- **Documentação completa**: `docs/DOCS.md`
- **Contexto da API**: `docs/api_context.json`
- **README principal**: `README.md`

### Comandos de ajuda
```bash
make help              # Lista todos os comandos disponíveis
make version           # Mostra versões
python3 run.py --help  # Ajuda do script de inicialização
```

### Links úteis
- **Issues**: https://github.com/noejunior792/hdl-ai-proteus/issues
- **Discussions**: https://github.com/noejunior792/hdl-ai-proteus/discussions

---

**🎯 Dica**: Para uma experiência mais rápida, use `make quick-start` na primeira vez e depois `make run` para inicializações subsequentes.