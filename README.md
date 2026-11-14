# Digital Insomnia API

API de um MVP acadêmico que utiliza um modelo de classificação para estimar uma categoria de dívida de sono a partir de hábitos digitais e informações do ambiente de descanso.

O projeto recebe os mesmos campos usados como features no treinamento do modelo, executa a previsão e retorna uma classe. O modelo é treinado no Google Colab e carregado pela API como um arquivo .joblib.

## Dataset e treinamento

O dataset foi obtido no Kaggle usando o KaggleHub:

- [Digital Insomnia: Screen Habits & Sleep](https://www.kaggle.com/datasets/beamhonor0911/digital-insomnia-screen-habits-sleep)
- [Notebook de treinamento no Google Colab](https://colab.research.google.com/drive/1CzicFqIJ3S18FeyLlICwbH2QeCY9-Q7P?usp=sharing)

O notebook realiza o pré-processamento e treina um classificador. Ao final, exporta o pipeline completo — incluindo as transformações e o classificador — com:

    joblib.dump(model, "sleep_debt_pipeline.joblib")

O alvo tem três classes: No Debt, Mild e Moderate/Severe. As categorias Moderate e Severe foram agrupadas porque o dataset contém poucos exemplos Severe.

**Limitação:** a página do dataset informa que os registros foram gerados por simulação. Portanto, o modelo aprende padrões desses dados simulados; os resultados não comprovam relações sobre pessoas reais e não devem ser usados para diagnóstico ou orientação médica.

## Como a API recebe uma previsão

O endpoint POST /digital-insomnia/predict recebe um objeto JSON com as 14 features usadas no treinamento:

    {
      "age": 28,
      "gender": "Female",
      "chronotype": "Night Owl",
      "occupation": "Professional",
      "bedtime_hour": 23.5,
      "screen_time_before_bed_min": 90,
      "primary_app_category": "Social Media",
      "screen_brightness_pct": 65,
      "blue_light_filter_on": true,
      "caffeine_intake_mg": 120,
      "caffeine_last_hour": 16.0,
      "physical_activity_min": 30,
      "room_temperature_f": 69.5,
      "ambient_noise_db": 32.0
    }

Uma resposta bem-sucedida tem este formato:

    {
      "prediction": "Mild"
    }

A documentação interativa do Flask-RESTX fica em:

    http://127.0.0.1:5000/digital-insomnia/docs

## Configuração do modelo

A API procura o artefato local em:

    artifacts/sleep_debt_pipeline.joblib

### Usar um arquivo local

Baixe o arquivo gerado pelo Colab e coloque-o nesse caminho. Se a pasta artifacts/ não existir, a API a cria durante a inicialização.

### Baixar o modelo automaticamente

Também é possível configurar um link HTTPS direto para o arquivo. Se o artefato local não existir, a API tenta baixá-lo ao iniciar:

    $env:SLEEP_MODEL_URL = "https://seu-host/sleep_debt_pipeline.joblib"
    $env:SLEEP_MODEL_SHA256 = "hash-sha256-do-arquivo"

SLEEP_MODEL_SHA256 é opcional, mas permite verificar a integridade do arquivo baixado. Use somente um artefato de uma origem confiável: carregar arquivos joblib de terceiros pode executar código.

Se não houver arquivo local nem SLEEP_MODEL_URL, a API inicia com um aviso, mas as previsões ficam indisponíveis até o modelo ser colocado em artifacts/ ou uma URL ser configurada.

## Instalação e execução

Requisitos: Python 3.12 ou compatível com as dependências listadas em requirements.txt.

No PowerShell, a partir da pasta do projeto:

    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python app.py

Com o servidor em execução, envie uma requisição POST para:

    http://127.0.0.1:5000/digital-insomnia/predict

O corpo deve ser JSON e conter todas as features indicadas no exemplo. O pipeline carregado aplica o mesmo pré-processamento usado no treinamento.

## Testes

Com o ambiente virtual ativado e a partir da raiz do projeto:

    pytest

A configuração em pytest.ini aponta o pytest para a raiz do projeto e descobre os testes na pasta test/.

## Estrutura principal

    app.py
    controller/
      sleep_prediction_controller.py
    model/
      request/
        sleep_request.py
    service/
      sleep_prediction_service.py
    artifacts/
      sleep_debt_pipeline.joblib
    test/
      sleep_prediction_test.py

