"""
Todo o conteúdo do site num lugar só.
Troque os textos abaixo pelos da sua empresa: os templates leem daqui.
"""

EMPRESA = {
    "nome": "Cobalto",
    "sufixo": "Software House",
    "slogan": "Software que sustenta a sua operação.",
    "email": "contato@cobalto.dev",
    "telefone": "(11) 4000-2026",
    "fundacao": 2014,
    "pessoas": 42,
    "projetos": 180,
}

SOLUCOES = [
    {
        "slug": "sistemas-web",
        "nome": "Sistemas web sob medida",
        "resumo": "Plataformas, portais e sistemas internos desenhados em torno do seu processo, não de um modelo pronto.",
        "descricao": (
            "Quando nenhuma ferramenta de prateleira cabe na sua operação, a gente constrói a que cabe. "
            "Começamos entendendo como o trabalho acontece hoje e entregamos um sistema que a sua equipe "
            "realmente quer usar, com painel administrativo, perfis de acesso e relatórios desde a primeira versão."
        ),
        "entregas": [
            "Portais de clientes e de fornecedores",
            "Sistemas de gestão (ERP, CRM, backoffice)",
            "Painéis administrativos com permissões por perfil",
            "Fluxos de aprovação e automação de rotinas manuais",
        ],
        "tecnologias": ["Python", "Django", "React", "PostgreSQL"],
    },
    {
        "slug": "apps-mobile",
        "nome": "Aplicativos mobile",
        "resumo": "Apps para iOS e Android com uma base de código só, rápidos e prontos para as lojas.",
        "descricao": (
            "Criamos aplicativos para clientes e para equipes de campo. Usamos uma base única para as duas "
            "plataformas, o que reduz prazo e custo de manutenção, e cuidamos de tudo até a publicação: "
            "contas nas lojas, revisão, versões e atualizações."
        ),
        "entregas": [
            "Apps para clientes com login, pagamentos e notificações",
            "Apps offline para equipes em campo",
            "Publicação e manutenção nas lojas",
            "Métricas de uso e de estabilidade",
        ],
        "tecnologias": ["Flutter", "React Native", "Firebase"],
    },
    {
        "slug": "apis-integracoes",
        "nome": "APIs e integrações",
        "resumo": "Ligamos os seus sistemas entre si e aos serviços externos, sem planilha no meio do caminho.",
        "descricao": (
            "Notas fiscais, meios de pagamento, transportadoras, marketplaces, sistemas legados: cada um fala "
            "uma língua diferente. Construímos as pontes entre eles, com monitoramento e reprocessamento "
            "automático quando algo falha."
        ),
        "entregas": [
            "APIs REST e GraphQL documentadas",
            "Integração com gateways de pagamento, ERPs e marketplaces",
            "Filas e processamento em segundo plano",
            "Painel de monitoramento das integrações",
        ],
        "tecnologias": ["Django REST", "Celery", "RabbitMQ", "Webhooks"],
    },
    {
        "slug": "dados-dashboards",
        "nome": "Dados e dashboards",
        "resumo": "Números confiáveis, atualizados e na tela de quem precisa decidir.",
        "descricao": (
            "Juntamos os dados espalhados pela empresa em um só lugar e montamos painéis que respondem às "
            "perguntas do dia a dia: quanto vendemos, onde estamos perdendo prazo, o que vai faltar no estoque."
        ),
        "entregas": [
            "Pipelines de dados e rotinas de carga",
            "Dashboards de vendas, operação e financeiro",
            "Alertas automáticos por e-mail e mensagem",
            "Modelos de previsão de demanda",
        ],
        "tecnologias": ["PostgreSQL", "dbt", "Metabase", "Python"],
    },
    {
        "slug": "modernizacao",
        "nome": "Modernização de sistemas legados",
        "resumo": "Tiramos o sistema antigo do caminho sem parar a operação.",
        "descricao": (
            "Aquele sistema que ninguém mais sabe mexer, mas que roda a empresa. Mapeamos o que ele faz, "
            "migramos por partes e mantemos os dois funcionando lado a lado até o novo assumir por completo."
        ),
        "entregas": [
            "Diagnóstico técnico e mapa de riscos",
            "Migração gradual, módulo por módulo",
            "Migração de dados com validação",
            "Documentação e treinamento da equipe",
        ],
        "tecnologias": ["Python", "Django", "Docker", "AWS"],
    },
    {
        "slug": "squad-dedicado",
        "nome": "Squad dedicado",
        "resumo": "Um time completo trabalhando como extensão da sua empresa, com custo mensal previsível.",
        "descricao": (
            "Para quem tem um produto em evolução constante. Montamos um time com desenvolvimento, design e "
            "qualidade, alinhado às suas prioridades, com reuniões semanais e entregas a cada quinzena."
        ),
        "entregas": [
            "Time multidisciplinar de 3 a 8 pessoas",
            "Planejamento e revisão a cada duas semanas",
            "Transferência de conhecimento contínua",
            "Escala do time para cima ou para baixo, conforme a fase",
        ],
        "tecnologias": ["Scrum", "CI/CD", "Testes automatizados"],
    },
]

PROCESSO = [
    {
        "titulo": "Descoberta",
        "texto": "Conversamos com quem usa o sistema e com quem decide. Saímos com o problema escrito e um escopo que cabe no orçamento.",
        "prazo": "1 a 2 semanas",
    },
    {
        "titulo": "Desenho",
        "texto": "Protótipos clicáveis e arquitetura definida. Você vê e testa as telas antes de escrevermos o código.",
        "prazo": "2 a 3 semanas",
    },
    {
        "titulo": "Construção",
        "texto": "Entregas a cada duas semanas, em produção ou em ambiente de testes. Você acompanha o progresso de perto.",
        "prazo": "6 a 16 semanas",
    },
    {
        "titulo": "Evolução",
        "texto": "Depois do lançamento continuamos ao lado: monitoramento, correções e novas funcionalidades.",
        "prazo": "Contínuo",
    },
]

CASES = [
    {
        "cliente": "Nortão Logística",
        "setor": "Transporte e logística",
        "titulo": "Roteirização de entregas em tempo real",
        "resumo": "Sistema que reorganiza as rotas dos motoristas ao longo do dia, conforme trânsito e novos pedidos.",
        "resultado": "31%",
        "resultado_texto": "menos custo por entrega",
        "cor": "cobalto",
    },
    {
        "cliente": "Clínica Vivare",
        "setor": "Saúde",
        "titulo": "Agendamento e prontuário no celular",
        "resumo": "App para pacientes marcarem consultas e para médicos consultarem o histórico durante o atendimento.",
        "resultado": "58 mil",
        "resultado_texto": "consultas marcadas pelo app em 12 meses",
        "cor": "tinta",
    },
    {
        "cliente": "Aurora Pagamentos",
        "setor": "Fintech",
        "titulo": "Conciliação financeira automática",
        "resumo": "Integração com sete bancos e adquirentes que fecha o caixa do dia sem intervenção manual.",
        "resultado": "4 h → 6 min",
        "resultado_texto": "para fechar o caixa diário",
        "cor": "sinal",
    },
]

VALORES = [
    {
        "titulo": "Clareza antes de código",
        "texto": "Escrevemos o problema em palavras simples antes de abrir o editor. Se não cabe em um parágrafo, ainda não está entendido.",
    },
    {
        "titulo": "Entrega pequena e frequente",
        "texto": "Preferimos mostrar algo funcionando a cada duas semanas a sumir por três meses e voltar com uma surpresa.",
    },
    {
        "titulo": "Código feito para durar",
        "texto": "Testes, revisão em par e documentação são parte do preço. Quem assumir o projeto depois entende o que foi feito.",
    },
    {
        "titulo": "Conversa direta",
        "texto": "Você fala com quem constrói. Sem intermediários, sem jargão e sem esconder o que deu errado.",
    },
]

MARCOS = [
    {"ano": "2014", "texto": "Três amigos de faculdade abrem a Cobalto numa sala emprestada, com um único cliente: uma rede de farmácias."},
    {"ano": "2017", "texto": "Chegamos a 15 pessoas e criamos a área de aplicativos mobile."},
    {"ano": "2020", "texto": "Passamos a trabalhar 100% remoto. Contratamos em todo o Brasil e o time dobra em dois anos."},
    {"ano": "2023", "texto": "Lançamos o modelo de squad dedicado e ultrapassamos 150 projetos entregues."},
    {"ano": "2026", "texto": "Somos 42 pessoas, com clientes em logística, saúde, varejo e serviços financeiros."},
]

TIME = [
    {"nome": "Marina Tavares", "cargo": "CEO e cofundadora", "iniciais": "MT"},
    {"nome": "Rafael Duarte", "cargo": "CTO e cofundador", "iniciais": "RD"},
    {"nome": "Helena Bastos", "cargo": "Diretora de produto e design", "iniciais": "HB"},
    {"nome": "Caio Nogueira", "cargo": "Líder de engenharia", "iniciais": "CN"},
]
