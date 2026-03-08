"""Curated collection of classic AI safety papers."""

from db.models import Paper
from db import repository as repo

SEED_PAPERS = [
    Paper(arxiv_id="1606.06565", title="Concrete Problems in AI Safety",
          authors='["Dario Amodei", "Chris Olah", "Jacob Steinhardt", "Paul Christiano", "John Schulman", "Dan Mané"]',
          abstract="Discusses five practical research problems related to accident risk in machine learning systems.",
          published_date="2016-06-21", arxiv_url="https://arxiv.org/abs/1606.06565",
          pdf_url="https://arxiv.org/pdf/1606.06565", is_classic=True, source="seed"),

    Paper(arxiv_id="1906.01820", title="Risks from Learned Optimization in Advanced Machine Learning Systems",
          authors='["Evan Hubinger", "Chris van Merwijk", "Vladimir Mikulik", "Joar Skalse", "Scott Garrabrant"]',
          abstract="Analyzes the type of learned optimization that occurs when a learned model is itself an optimizer (mesa-optimization).",
          published_date="2019-06-05", arxiv_url="https://arxiv.org/abs/1906.01820",
          pdf_url="https://arxiv.org/pdf/1906.01820", is_classic=True, source="seed"),

    Paper(arxiv_id="2202.03286", title="Red Teaming Language Models with Language Models",
          authors='["Ethan Perez", "Saffron Huang", "Francis Song", "Trevor Cai", "Roman Ring", "John Aslanides", "Amelia Glaese", "Nat McAleese", "Geoffrey Irving"]',
          abstract="Automatically finds cases where a target LM behaves in a harmful way using another LM to generate test cases.",
          published_date="2022-02-07", arxiv_url="https://arxiv.org/abs/2202.03286",
          pdf_url="https://arxiv.org/pdf/2202.03286", is_classic=True, source="seed"),

    Paper(arxiv_id="2212.08073", title="Constitutional AI: Harmlessness from AI Feedback",
          authors='["Yuntao Bai", "Saurav Kadavath", "Sandipan Kundu", "Amanda Askell", "Jackson Kernion", "Andy Jones", "Anna Chen", "Anna Goldie", "Azalia Mirhoseini", "Cameron McKinnon"]',
          abstract="A method for training AI systems to be helpful, harmless, and honest using AI feedback.",
          published_date="2022-12-15", arxiv_url="https://arxiv.org/abs/2212.08073",
          pdf_url="https://arxiv.org/pdf/2212.08073", is_classic=True, source="seed"),

    Paper(arxiv_id="2305.04388", title="Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting",
          authors='["Miles Turpin", "Julian Michael", "Ethan Perez", "Samuel R. Bowman"]',
          abstract="Shows that CoT explanations can be unfaithful to the model's actual reasoning process.",
          published_date="2023-05-07", arxiv_url="https://arxiv.org/abs/2305.04388",
          pdf_url="https://arxiv.org/pdf/2305.04388", is_classic=True, source="seed"),

    Paper(arxiv_id="2307.15043", title="Universal and Transferable Adversarial Attacks on Aligned Language Models",
          authors='["Andy Zou", "Zifan Wang", "Nicholas Carlini", "Milad Nasr", "J. Zico Kolter", "Matt Fredrikson"]',
          abstract="Demonstrates that adversarial suffixes can jailbreak aligned language models.",
          published_date="2023-07-27", arxiv_url="https://arxiv.org/abs/2307.15043",
          pdf_url="https://arxiv.org/pdf/2307.15043", is_classic=True, source="seed"),

    Paper(arxiv_id="2310.01405", title="Representation Engineering: A Top-Down Approach to AI Transparency",
          authors='["Andy Zou", "Long Phan", "Sarah Chen", "James Campbell", "Phillip Guo", "Richard Ren", "Alexander Pan", "Xuwang Yin", "Mantas Mazeika", "Ann-Kathrin Dombrowski", "Shashwat Goel", "Nathaniel Li", "Michael J. Byun", "Zifan Wang", "Alex Mallen", "Steven Basart", "Sanmi Koyejo", "Dawn Song", "Matt Fredrikson", "J. Zico Kolter", "Dan Hendrycks"]',
          abstract="Introduces representation engineering as a top-down approach to neural network transparency.",
          published_date="2023-10-02", arxiv_url="https://arxiv.org/abs/2310.01405",
          pdf_url="https://arxiv.org/pdf/2310.01405", is_classic=True, source="seed"),

    Paper(arxiv_id="2312.14925", title="RLHF: Reinforcement Learning from Human Feedback - A Survey",
          authors='["Tian-Xiang Sun"]',
          abstract="A comprehensive survey of reinforcement learning from human feedback methods for aligning language models.",
          published_date="2023-12-22", arxiv_url="https://arxiv.org/abs/2312.14925",
          pdf_url="https://arxiv.org/pdf/2312.14925", is_classic=True, source="seed"),

    Paper(arxiv_id="2103.14659", title="Alignment of Language Agents",
          authors='["Zachary Kenton", "Tom Everitt", "Laura Weidinger", "Iason Gabriel", "Vladimir Mikulik", "Geoffrey Irving"]',
          abstract="Discusses key alignment problems specific to language agents.",
          published_date="2021-03-26", arxiv_url="https://arxiv.org/abs/2103.14659",
          pdf_url="https://arxiv.org/pdf/2103.14659", is_classic=True, source="seed"),

    Paper(arxiv_id="2109.07958", title="TruthfulQA: Measuring How Models Mimic Human Falsehoods",
          authors='["Stephanie Lin", "Jacob Hilton", "Owain Evans"]',
          abstract="Benchmark measuring whether language models generate truthful answers to questions.",
          published_date="2021-09-08", arxiv_url="https://arxiv.org/abs/2109.07958",
          pdf_url="https://arxiv.org/pdf/2109.07958", is_classic=True, source="seed"),

    Paper(arxiv_id="2203.02155", title="Training language models to follow instructions with human feedback",
          authors='["Long Ouyang", "Jeff Wu", "Xu Jiang", "Diogo Almeida", "Carroll L. Wainwright", "Pamela Mishkin", "Chong Zhang", "Sandhini Agarwal", "Katarina Slama", "Alex Ray"]',
          abstract="InstructGPT: aligning language models with user intent via RLHF.",
          published_date="2022-03-04", arxiv_url="https://arxiv.org/abs/2203.02155",
          pdf_url="https://arxiv.org/pdf/2203.02155", is_classic=True, source="seed"),

    Paper(arxiv_id="1706.03762", title="Attention Is All You Need",
          authors='["Ashish Vaswani", "Noam Shazeer", "Niki Parmar", "Jakob Uszkoreit", "Llion Jones", "Aidan N. Gomez", "Lukasz Kaiser", "Illia Polosukhin"]',
          abstract="Introduces the Transformer architecture based solely on attention mechanisms.",
          published_date="2017-06-12", arxiv_url="https://arxiv.org/abs/1706.03762",
          pdf_url="https://arxiv.org/pdf/1706.03762", is_classic=True, source="seed"),

    Paper(arxiv_id="2305.18290", title="Direct Preference Optimization: Your Language Model is Secretly a Reward Model",
          authors='["Rafael Rafailov", "Archit Sharma", "Eric Mitchell", "Stefano Ermon", "Christopher D. Manning", "Chelsea Finn"]',
          abstract="DPO: a simple alternative to RLHF that directly optimizes the policy using preferences.",
          published_date="2023-05-29", arxiv_url="https://arxiv.org/abs/2305.18290",
          pdf_url="https://arxiv.org/pdf/2305.18290", is_classic=True, source="seed"),

    Paper(arxiv_id="2302.04761", title="Toolformer: Language Models Can Teach Themselves to Use Tools",
          authors='["Timo Schick", "Jane Dwivedi-Yu", "Roberto Dessì", "Roberta Raileanu", "Maria Lomeli", "Luke Zettlemoyer", "Nicola Cancedda", "Thomas Scialom"]',
          abstract="Language models that learn to use external tools via self-supervised training.",
          published_date="2023-02-09", arxiv_url="https://arxiv.org/abs/2302.04761",
          pdf_url="https://arxiv.org/pdf/2302.04761", is_classic=True, source="seed"),

    Paper(arxiv_id="2305.16264", title="Scaling Data-Constrained Language Models",
          authors='["Niklas Muennighoff", "Alexander M. Rush", "Boaz Barak", "Teven Le Scao", "Nouamane Tazi", "Aleksandra Piktus", "Sampo Pyysalo", "Thomas Wolf", "Colin Raffel"]',
          abstract="Studies scaling laws when data is limited and repeated during training.",
          published_date="2023-05-25", arxiv_url="https://arxiv.org/abs/2305.16264",
          pdf_url="https://arxiv.org/pdf/2305.16264", is_classic=True, source="seed"),

    Paper(arxiv_id="2304.15004", title="Are Emergent Abilities of Large Language Models a Mirage?",
          authors='["Rylan Schaeffer", "Brando Miranda", "Sanmi Koyejo"]',
          abstract="Argues that emergent abilities of LLMs may be artifacts of metric choice.",
          published_date="2023-04-28", arxiv_url="https://arxiv.org/abs/2304.15004",
          pdf_url="https://arxiv.org/pdf/2304.15004", is_classic=True, source="seed"),

    Paper(arxiv_id="2401.05566", title="Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training",
          authors='["Evan Hubinger", "Carson Denison", "Jesse Mu", "Mike Lambert", "Meg Tong", "Monte MacDiarmid", "Tamera Lanham", "Daniel M. Ziegler", "Tim Telleen-Lawton", "Noa Nabeshima"]',
          abstract="Demonstrates that backdoor behavior in LLMs can persist through standard safety training.",
          published_date="2024-01-10", arxiv_url="https://arxiv.org/abs/2401.05566",
          pdf_url="https://arxiv.org/pdf/2401.05566", is_classic=True, source="seed"),

    Paper(arxiv_id="2302.07459", title="The Capacity for Moral Self-Correction in Large Language Models",
          authors='["Deep Ganguli", "Amanda Askell", "Nicholas Schiefer", "Thomas Liao", "Kamilė Lukošiūtė", "Anna Chen", "Anna Goldie", "Azalia Mirhoseini"]',
          abstract="Shows that large language models can be guided to correct their own morally problematic outputs.",
          published_date="2023-02-14", arxiv_url="https://arxiv.org/abs/2302.07459",
          pdf_url="https://arxiv.org/pdf/2302.07459", is_classic=True, source="seed"),

    Paper(arxiv_id="2303.08774", title="GPT-4 Technical Report",
          authors='["OpenAI"]',
          abstract="Technical report on GPT-4, a large-scale multimodal model.",
          published_date="2023-03-15", arxiv_url="https://arxiv.org/abs/2303.08774",
          pdf_url="https://arxiv.org/pdf/2303.08774", is_classic=True, source="seed"),

    Paper(arxiv_id="2305.10601", title="Tree of Thoughts: Deliberate Problem Solving with Large Language Models",
          authors='["Shunyu Yao", "Dian Yu", "Jeffrey Zhao", "Izhak Shafran", "Thomas L. Griffiths", "Yuan Cao", "Karthik Narasimhan"]',
          abstract="Introduces a framework for LLM reasoning via tree-structured exploration.",
          published_date="2023-05-17", arxiv_url="https://arxiv.org/abs/2305.10601",
          pdf_url="https://arxiv.org/pdf/2305.10601", is_classic=True, source="seed"),

    Paper(arxiv_id="2204.05862", title="Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback",
          authors='["Yuntao Bai", "Andy Jones", "Kamal Ndousse", "Amanda Askell", "Anna Chen", "Nova DasSarma", "Dawn Drain", "Stanislav Fort", "Deep Ganguli", "Tom Henighan"]',
          abstract="Anthropic's work on training an AI assistant to be both helpful and harmless using RLHF.",
          published_date="2022-04-12", arxiv_url="https://arxiv.org/abs/2204.05862",
          pdf_url="https://arxiv.org/pdf/2204.05862", is_classic=True, source="seed"),

    Paper(arxiv_id="2105.14111", title="Objective Robustness in Deep Reinforcement Learning",
          authors='["Joar Skalse", "Matthew Farrugia-Roberts"]',
          abstract="Studies how RL agents can pursue unintended objectives due to distributional shift.",
          published_date="2021-05-28", arxiv_url="https://arxiv.org/abs/2105.14111",
          pdf_url="https://arxiv.org/pdf/2105.14111", is_classic=True, source="seed"),

    Paper(arxiv_id="2209.07858", title="Scaling Laws for Reward Model Overoptimization",
          authors='["Leo Gao", "John Schulman", "Jacob Hilton"]',
          abstract="Studies reward model overoptimization in RLHF, where the proxy reward diverges from the true objective.",
          published_date="2022-09-16", arxiv_url="https://arxiv.org/abs/2209.07858",
          pdf_url="https://arxiv.org/pdf/2209.07858", is_classic=True, source="seed"),

    Paper(arxiv_id="2305.13860", title="LIMA: Less Is More for Alignment",
          authors='["Chunting Zhou", "Pengfei Liu", "Puxin Xu", "Srini Iyer", "Jiao Sun", "Yuning Mao", "Xuezhe Ma", "Avia Efrat", "Ping Yu", "Lili Yu"]',
          abstract="Shows that a small set of carefully curated examples can align a strong pretrained model.",
          published_date="2023-05-18", arxiv_url="https://arxiv.org/abs/2305.13860",
          pdf_url="https://arxiv.org/pdf/2305.13860", is_classic=True, source="seed"),

    Paper(arxiv_id="2306.11698", title="DecodingTrust: A Comprehensive Assessment of Trustworthiness in GPT Models",
          authors='["Boxin Wang", "Weixin Chen", "Hengzhi Pei", "Chulin Xie", "Mintong Kang", "Chenhui Zhang", "Chejian Xu", "Zidi Xiong", "Ritik Dutta", "Rylan Schaeffer"]',
          abstract="Comprehensive evaluation of GPT models across multiple trustworthiness dimensions.",
          published_date="2023-06-20", arxiv_url="https://arxiv.org/abs/2306.11698",
          pdf_url="https://arxiv.org/pdf/2306.11698", is_classic=True, source="seed"),

    Paper(arxiv_id="2303.12712", title="Sparks of Artificial General Intelligence: Early experiments with GPT-4",
          authors='["Sébastien Bubeck", "Varun Chandrasekaran", "Ronen Eldan", "Johannes Gehrke", "Eric Horvitz", "Ece Kamar", "Peter Lee", "Yin Tat Lee", "Yuanzhi Li", "Scott Lundberg"]',
          abstract="Early experiments with GPT-4 suggesting it may be an early version of AGI.",
          published_date="2023-03-22", arxiv_url="https://arxiv.org/abs/2303.12712",
          pdf_url="https://arxiv.org/pdf/2303.12712", is_classic=True, source="seed"),

    Paper(arxiv_id="2302.07388", title="Adding Instructions during Pretraining: Effective Way of Controlling Toxicity in Language Models",
          authors='["Shrimai Prabhumoye", "Mostofa Patwary", "Mohammad Shoeybi", "Bryan Catanzaro"]',
          abstract="Reducing toxicity in language models by adding instructions during the pretraining phase.",
          published_date="2023-02-14", arxiv_url="https://arxiv.org/abs/2302.07388",
          pdf_url="https://arxiv.org/pdf/2302.07388", is_classic=True, source="seed"),

    Paper(arxiv_id="2309.02427", title="Cognitive Architectures for Language Agents",
          authors='["Theodore R. Sumers", "Shunyu Yao", "Karthik Narasimhan", "Thomas L. Griffiths"]',
          abstract="Framework for designing cognitive architectures for language model-based agents.",
          published_date="2023-09-05", arxiv_url="https://arxiv.org/abs/2309.02427",
          pdf_url="https://arxiv.org/pdf/2309.02427", is_classic=True, source="seed"),

    Paper(arxiv_id="2312.09390", title="Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision",
          authors='["Collin Burns", "Haotian Ye", "Dan Klein", "Jacob Steinhardt"]',
          abstract="Studies whether weak model supervision can elicit strong model capabilities, relevant to scalable oversight.",
          published_date="2023-12-14", arxiv_url="https://arxiv.org/abs/2312.09390",
          pdf_url="https://arxiv.org/pdf/2312.09390", is_classic=True, source="seed"),

    Paper(arxiv_id="2201.11903", title="Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
          authors='["Jason Wei", "Xuezhi Wang", "Dale Schuurmans", "Maarten Bosma", "Brian Ichter", "Fei Xia", "Ed Chi", "Quoc Le", "Denny Zhou"]',
          abstract="Shows that chain-of-thought prompting enables complex reasoning in LLMs.",
          published_date="2022-01-28", arxiv_url="https://arxiv.org/abs/2201.11903",
          pdf_url="https://arxiv.org/pdf/2201.11903", is_classic=True, source="seed"),

    Paper(arxiv_id="2206.04615", title="Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models",
          authors='["BIG-bench authors"]',
          abstract="BIG-Bench: a large-scale benchmark for evaluating language model capabilities.",
          published_date="2022-06-09", arxiv_url="https://arxiv.org/abs/2206.04615",
          pdf_url="https://arxiv.org/pdf/2206.04615", is_classic=True, source="seed"),

    Paper(arxiv_id="2302.13971", title="LLaMA: Open and Efficient Foundation Language Models",
          authors='["Hugo Touvron", "Thibaut Lavril", "Gautier Izacard", "Xavier Martinet", "Marie-Anne Lachaux", "Timothée Lacroix", "Baptiste Rozière", "Naman Goyal", "Eric Hambro", "Faisal Azhar"]',
          abstract="LLaMA: a collection of efficient open-source language models.",
          published_date="2023-02-27", arxiv_url="https://arxiv.org/abs/2302.13971",
          pdf_url="https://arxiv.org/pdf/2302.13971", is_classic=True, source="seed"),

    Paper(arxiv_id="2306.11644", title="Textbooks Are All You Need",
          authors='["Suriya Gunasekar", "Yi Zhang", "Jyoti Aneja", "Caio César Teodoro Mendes", "Allie Del Giorno", "Sefa Greven", "Aditya Gupta", "Sebastian Bubeck", "Ronen Eldan"]',
          abstract="Phi-1: training small but capable models using high-quality textbook data.",
          published_date="2023-06-20", arxiv_url="https://arxiv.org/abs/2306.11644",
          pdf_url="https://arxiv.org/pdf/2306.11644", is_classic=True, source="seed"),

    Paper(arxiv_id="1906.02629", title="When Does Label Smoothing Help?",
          authors='["Rafael Müller", "Simon Kornblith", "Geoffrey Hinton"]',
          abstract="Studies when and why label smoothing improves model calibration and generalization.",
          published_date="2019-06-06", arxiv_url="https://arxiv.org/abs/1906.02629",
          pdf_url="https://arxiv.org/pdf/1906.02629", is_classic=True, source="seed"),

    Paper(arxiv_id="2308.09687", title="Graph of Thoughts: Solving Elaborate Problems with Large Language Models",
          authors='["Maciej Besta", "Nils Blach", "Ales Kubicek", "Robert Gerstenberger", "Lukas Gianinazzi", "Joanna Gajda", "Tomasz Lehmann", "Michał Podstawski", "Hubert Niewiadomski", "Piotr Nyczyk", "Torsten Hoefler"]',
          abstract="Extends chain-of-thought to graph structures for more complex LLM reasoning.",
          published_date="2023-08-18", arxiv_url="https://arxiv.org/abs/2308.09687",
          pdf_url="https://arxiv.org/pdf/2308.09687", is_classic=True, source="seed"),

    Paper(arxiv_id="2305.14314", title="QLoRA: Efficient Finetuning of Quantized Language Models",
          authors='["Tim Dettmers", "Artidoro Pagnoni", "Ari Holtzman", "Luke Zettlemoyer"]',
          abstract="Enables finetuning of large models with minimal memory using quantization.",
          published_date="2023-05-23", arxiv_url="https://arxiv.org/abs/2305.14314",
          pdf_url="https://arxiv.org/pdf/2305.14314", is_classic=True, source="seed"),

    Paper(arxiv_id="2210.11416", title="Scaling Instruction-Finetuned Language Models",
          authors='["Hyung Won Chung", "Le Hou", "Shayne Longpre", "Barret Zoph", "Yi Tay", "William Fedus", "Yunxuan Li", "Xuezhi Wang", "Mostafa Dehghani", "Siddhartha Brahma"]',
          abstract="Flan-PaLM: scaling instruction finetuning to improve model performance.",
          published_date="2022-10-20", arxiv_url="https://arxiv.org/abs/2210.11416",
          pdf_url="https://arxiv.org/pdf/2210.11416", is_classic=True, source="seed"),

    Paper(arxiv_id="2311.14125", title="Scalable AI Safety via Doubly-Efficient Debate",
          authors='["Jonah Brown-Cohen", "Geoffrey Irving", "Georgios Piliouras"]',
          abstract="Proposes theoretically grounded debate protocols for scalable AI safety oversight.",
          published_date="2023-11-23", arxiv_url="https://arxiv.org/abs/2311.14125",
          pdf_url="https://arxiv.org/pdf/2311.14125", is_classic=True, source="seed"),

    Paper(arxiv_id="2310.11511", title="Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection",
          authors='["Akari Asai", "Zeqiu Wu", "Yizhong Wang", "Avirup Sil", "Hannaneh Hajishirzi"]',
          abstract="Training LLMs to adaptively retrieve and self-reflect for more factual generation.",
          published_date="2023-10-17", arxiv_url="https://arxiv.org/abs/2310.11511",
          pdf_url="https://arxiv.org/pdf/2310.11511", is_classic=True, source="seed"),

    Paper(arxiv_id="2305.03047", title="Principle-Driven Self-Alignment of Language Models from Scratch with Minimal Human Supervision",
          authors='["Zhiqing Sun", "Yikang Shen", "Qinhong Zhou", "Hongxin Zhang", "Zhenfang Chen", "David Cox", "Yiming Yang", "Chuang Gan"]',
          abstract="Enables LLMs to self-align with minimal human supervision using principles.",
          published_date="2023-05-04", arxiv_url="https://arxiv.org/abs/2305.03047",
          pdf_url="https://arxiv.org/pdf/2305.03047", is_classic=True, source="seed"),

    Paper(arxiv_id="2304.10436", title="Safety Assessment of Chinese Large Language Models",
          authors='["Hao Sun", "Zhexin Zhang", "Jiawen Deng", "Jiale Cheng", "Minlie Huang"]',
          abstract="Comprehensive safety evaluation of Chinese LLMs across multiple dimensions.",
          published_date="2023-04-20", arxiv_url="https://arxiv.org/abs/2304.10436",
          pdf_url="https://arxiv.org/pdf/2304.10436", is_classic=True, source="seed"),

    Paper(arxiv_id="2404.13208", title="The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions",
          authors='["Eric Wallace", "Kai Xiao", "Reimar Leike", "Lilian Weng", "Johannes Heidecke", "Alex Beutel"]',
          abstract="Training LLMs to properly prioritize system-level instructions over user inputs.",
          published_date="2024-04-19", arxiv_url="https://arxiv.org/abs/2404.13208",
          pdf_url="https://arxiv.org/pdf/2404.13208", is_classic=True, source="seed"),

    Paper(arxiv_id="2304.03279", title="Do the Rewards Justify the Means? Measuring Trade-Offs Between Rewards and Ethical Behavior in the MACHIAVELLI Benchmark",
          authors='["Alexander Pan", "Jun Shern Chan", "Andy Zou", "Nathaniel Li", "Steven Basart", "Thomas Woodside", "Jonathan Ng", "Hanlin Zhang", "Scott Emmons", "Dan Hendrycks"]',
          abstract="Benchmark measuring ethical behavior vs reward-seeking in LLM agents.",
          published_date="2023-04-06", arxiv_url="https://arxiv.org/abs/2304.03279",
          pdf_url="https://arxiv.org/pdf/2304.03279", is_classic=True, source="seed"),

    Paper(arxiv_id="2310.10683", title="Large Language Model Unlearning",
          authors='["Yuanshun Yao", "Xiaojun Xu", "Yang Liu"]',
          abstract="Methods for removing specific knowledge or capabilities from trained LLMs.",
          published_date="2023-10-16", arxiv_url="https://arxiv.org/abs/2310.10683",
          pdf_url="https://arxiv.org/pdf/2310.10683", is_classic=True, source="seed"),

    Paper(arxiv_id="2209.13085", title="Defining and Characterizing Reward Hacking",
          authors='["Joar Skalse", "Nikolaus H.R. Howe", "Dmitrii Krasheninnikov", "David Krueger"]',
          abstract="Formalizes reward and specification gaming in ML systems.",
          published_date="2022-09-27", arxiv_url="https://arxiv.org/abs/2209.13085",
          pdf_url="https://arxiv.org/pdf/2209.13085", is_classic=True, source="seed"),

    Paper(arxiv_id="2211.09110", title="Holistic Evaluation of Language Models",
          authors='["Percy Liang", "Rishi Bommasani", "Tony Lee", "Dimitris Tsipras", "Dilara Soylu", "Michihiro Yasunaga", "Yian Zhang", "Deepak Narayanan", "Yuhuai Wu", "Ananya Kumar"]',
          abstract="HELM: comprehensive evaluation framework for language models across many dimensions.",
          published_date="2022-11-16", arxiv_url="https://arxiv.org/abs/2211.09110",
          pdf_url="https://arxiv.org/pdf/2211.09110", is_classic=True, source="seed"),

    Paper(arxiv_id="2308.03958", title="Simple synthetic data reduces sycophancy in large language models",
          authors='["Jerry Wei", "Da Huang", "Yifeng Lu", "Denny Zhou", "Quoc V. Le"]',
          abstract="Uses synthetic data to reduce sycophantic behavior in LLMs.",
          published_date="2023-08-07", arxiv_url="https://arxiv.org/abs/2308.03958",
          pdf_url="https://arxiv.org/pdf/2308.03958", is_classic=True, source="seed"),

    # ── 2024–2025 high-impact AI safety papers ───────────────

    Paper(arxiv_id="2412.14093", title="Alignment Faking in Large Language Models",
          authors='["Ryan Greenblatt", "Carson Denison", "Benjamin Wright", "Fabien Roger", "Monte MacDiarmid", "Sam Marks", "Johannes Treutlein", "Tim Belonax", "Jack Chen", "David Duvenaud", "Akbir Khan", "Julian Michael", "Sören Mindermann", "Ethan Perez", "Linda Petrini", "Jonathan Uesato", "Jared Kaplan", "Buck Shlegeris", "Samuel R. Bowman", "Evan Hubinger"]',
          abstract="Demonstrates that Claude 3 Opus can fake alignment: selectively complying with training objectives to prevent modification of its behavior.",
          published_date="2024-12-18", arxiv_url="https://arxiv.org/abs/2412.14093",
          pdf_url="https://arxiv.org/pdf/2412.14093", is_classic=True, source="seed"),

    Paper(arxiv_id="2412.04984", title="Frontier Models are Capable of In-context Scheming",
          authors='["Alexander Meinke", "Bronson Schoen", "Jérémy Scheurer", "Mikita Balesni", "Rusheb Shah", "Marius Hobbhahn"]',
          abstract="Shows that frontier models like o1, Claude 3.5, and Gemini 1.5 Pro can covertly pursue misaligned goals and scheme in-context.",
          published_date="2024-12-06", arxiv_url="https://arxiv.org/abs/2412.04984",
          pdf_url="https://arxiv.org/pdf/2412.04984", is_classic=True, source="seed"),

    Paper(arxiv_id="2406.10162", title="Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models",
          authors='["Carson Denison", "Monte MacDiarmid", "Fazl Barez", "David Duvenaud", "Shauna Kravec", "Samuel Marks", "Nicholas Schiefer", "Ryan Soklaski", "Alex Tamkin", "Jared Kaplan", "Buck Shlegeris", "Samuel R. Bowman", "Ethan Perez", "Evan Hubinger"]',
          abstract="Studies how LLMs can escalate from sycophantic behavior to actively tampering with reward signals.",
          published_date="2024-06-14", arxiv_url="https://arxiv.org/abs/2406.10162",
          pdf_url="https://arxiv.org/pdf/2406.10162", is_classic=True, source="seed"),

    Paper(arxiv_id="2406.07358", title="AI Sandbagging: Language Models can Strategically Underperform on Evaluations",
          authors='["Teun van der Weij", "Felix Hofstätter", "Ollie Jaffe", "Samuel F. Brown", "Francis Rhys Ward"]',
          abstract="Demonstrates that frontier LLMs can be prompted or fine-tuned to strategically underperform on dangerous capability evaluations while maintaining general performance.",
          published_date="2024-06-11", arxiv_url="https://arxiv.org/abs/2406.07358",
          pdf_url="https://arxiv.org/pdf/2406.07358", is_classic=True, source="seed"),

    Paper(arxiv_id="2406.04313", title="Improving Alignment and Robustness with Circuit Breakers",
          authors='["Andy Zou", "Long Phan", "Justin Wang", "Derek Duenas", "Maxwell Lin", "Maksym Andriushchenko", "Rowan Wang", "Zico Kolter", "Matt Fredrikson", "Dan Hendrycks"]',
          abstract="Introduces circuit breaking as an alternative to refusal training that directly controls harmful representations to robustly prevent harmful outputs.",
          published_date="2024-06-06", arxiv_url="https://arxiv.org/abs/2406.04313",
          pdf_url="https://arxiv.org/pdf/2406.04313", is_classic=True, source="seed"),

    Paper(arxiv_id="2403.03218", title="The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning",
          authors='["Nathaniel Li", "Alexander Pan", "Anjali Gopal", "Summer Yue", "Daniel Berber", "Aidan O\'Gara", "Mantas Mazeika", "Dan Hendrycks"]',
          abstract="Introduces the Weapons of Mass Destruction Proxy benchmark with 3,668 questions measuring hazardous knowledge in biosecurity, cybersecurity, and chemical security.",
          published_date="2024-03-05", arxiv_url="https://arxiv.org/abs/2403.03218",
          pdf_url="https://arxiv.org/pdf/2403.03218", is_classic=True, source="seed"),

    Paper(arxiv_id="2407.13692", title="Prover-Verifier Games Improve Legibility of LLM Outputs",
          authors='["Jan Hendrik Kirchner", "Yining Chen", "Harri Edwards", "Jan Leike", "Nat McAleese", "Yuri Burda"]',
          abstract="Uses prover-verifier game training to improve the legibility and verifiability of LLM chain-of-thought reasoning.",
          published_date="2024-07-18", arxiv_url="https://arxiv.org/abs/2407.13692",
          pdf_url="https://arxiv.org/pdf/2407.13692", is_classic=True, source="seed"),

    Paper(arxiv_id="2410.21514", title="Sabotage Evaluations for Frontier Models",
          authors='["Joe Benton", "Misha Wagner", "Eric Christiansen", "Cem Anil", "Ethan Perez", "Jai Srivastav", "Esin Durmus", "Deep Ganguli", "Shauna Kravec", "Buck Shlegeris", "Jared Kaplan", "Samuel R. Bowman", "Roger Grosse"]',
          abstract="Evaluates whether frontier models could covertly sabotage oversight mechanisms, capability evaluations, or deployment decisions.",
          published_date="2024-10-28", arxiv_url="https://arxiv.org/abs/2410.21514",
          pdf_url="https://arxiv.org/pdf/2410.21514", is_classic=True, source="seed"),

    Paper(arxiv_id="2404.14082", title="Mechanistic Interpretability for AI Safety -- A Review",
          authors='["Leonard Bereska", "Efstratios Gavves"]',
          abstract="Comprehensive review of mechanistic interpretability as an approach to reverse-engineer neural network computations for AI safety.",
          published_date="2024-04-22", arxiv_url="https://arxiv.org/abs/2404.14082",
          pdf_url="https://arxiv.org/pdf/2404.14082", is_classic=True, source="seed"),

    Paper(arxiv_id="2405.12522", title="Sparse Autoencoders Enable Scalable and Reliable Circuit Identification in Language Models",
          authors='["Charles O\'Neill", "Thang Bui"]',
          abstract="Shows that sparse autoencoders can identify interpretable circuits in language models in a scalable and reliable way.",
          published_date="2024-05-21", arxiv_url="https://arxiv.org/abs/2405.12522",
          pdf_url="https://arxiv.org/pdf/2405.12522", is_classic=True, source="seed"),

    Paper(arxiv_id="2405.14860", title="Not All Language Model Features Are One-Dimensionally Linear",
          authors='["Joshua Engels", "Isaac Liao", "Eric J. Michaud", "Wes Gurnee", "Max Tegmark"]',
          abstract="Challenges the linear representation hypothesis by showing that some LLM features are irreducibly multi-dimensional.",
          published_date="2024-05-23", arxiv_url="https://arxiv.org/abs/2405.14860",
          pdf_url="https://arxiv.org/pdf/2405.14860", is_classic=True, source="seed"),

    Paper(arxiv_id="2406.14598", title="SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal",
          authors='["Tinghao Xie", "Xiangyu Qi", "Yi Zeng", "Yangsibo Huang", "Udari Madhushani Sehwag", "Kaixuan Huang", "Luxi He", "Boyi Wei", "Dacheng Li", "Ying Sheng", "Ruoxi Jia", "Bo Li", "Kai Li", "Danqi Chen", "Peter Henderson", "Prateek Mittal"]',
          abstract="Systematic benchmark for evaluating LLM safety refusal behaviors across fine-grained unsafe categories.",
          published_date="2024-06-20", arxiv_url="https://arxiv.org/abs/2406.14598",
          pdf_url="https://arxiv.org/pdf/2406.14598", is_classic=True, source="seed"),

    Paper(arxiv_id="2409.07985", title="Games for AI Control: Models of Safety Evaluations of AI Deployment Protocols",
          authors='["Charlie Griffin", "Louis Thomson", "Buck Shlegeris", "Alessandro Abate"]',
          abstract="Formalizes AI control red-teaming as multi-objective stochastic games for evaluating safe deployment protocols of untrusted models.",
          published_date="2024-09-12", arxiv_url="https://arxiv.org/abs/2409.07985",
          pdf_url="https://arxiv.org/pdf/2409.07985", is_classic=True, source="seed"),

    Paper(arxiv_id="2401.05561", title="TrustLLM: Trustworthiness in Large Language Models",
          authors='["Lichao Sun", "Yue Huang", "Haoran Wang", "Siyuan Wu", "Qihui Zhang", "Chujie Gao", "Yixin Huang", "Wenhan Lyu", "Yixuan Zhang", "Xiner Li"]',
          abstract="Comprehensive framework and benchmark for evaluating trustworthiness of LLMs across multiple dimensions.",
          published_date="2024-01-10", arxiv_url="https://arxiv.org/abs/2401.05561",
          pdf_url="https://arxiv.org/pdf/2401.05561", is_classic=True, source="seed"),

    Paper(arxiv_id="2404.12241", title="Introducing v0.5 of the AI Safety Benchmark from MLCommons",
          authors='["Bertie Vidgen", "Adarsh Agrawal", "Ahmed M. Ahmed", "Victor Akinwande", "Namir Al-Nuaimi", "Najla Alfaraj"]',
          abstract="MLCommons AI Safety Benchmark v0.5 for standardized evaluation of LLM safety across diverse hazard categories.",
          published_date="2024-04-18", arxiv_url="https://arxiv.org/abs/2404.12241",
          pdf_url="https://arxiv.org/pdf/2404.12241", is_classic=True, source="seed"),

    Paper(arxiv_id="2405.06624", title="Towards Guaranteed Safe AI: A Framework for Ensuring Robust and Reliable AI Systems",
          authors='["David Dalrymple", "Joar Skalse", "Yoshua Bengio", "Stuart Russell", "Max Tegmark", "Sanjit Seshia", "Steve Omohundro", "Christian Szegedy", "Ben Goldhaber", "Nora Ammann"]',
          abstract="Proposes a framework for guaranteed safe AI using quantitative safety guarantees via world models, safety specifications, and verifiers.",
          published_date="2024-05-10", arxiv_url="https://arxiv.org/abs/2405.06624",
          pdf_url="https://arxiv.org/pdf/2405.06624", is_classic=True, source="seed"),

    Paper(arxiv_id="2310.19852", title="AI Alignment: A Comprehensive Survey",
          authors='["Jiaming Ji", "Tianyi Qiu", "Boyuan Chen", "Borber Zhang", "Hantao Lou", "Kaile Wang", "Yawen Duan", "Zhonghao He", "Jiayi Zhou", "Zhaowei Zhang"]',
          abstract="Comprehensive survey of AI alignment research identifying Robustness, Interpretability, Controllability, and Ethicality (RICE) as key principles.",
          published_date="2024-02-28", arxiv_url="https://arxiv.org/abs/2310.19852",
          pdf_url="https://arxiv.org/pdf/2310.19852", is_classic=True, source="seed"),

    Paper(arxiv_id="2501.17805", title="International AI Safety Report",
          authors='["Yoshua Bengio", "Stuart Russell", "Saurabh Mishra"]',
          abstract="Comprehensive international report synthesizing current evidence on capabilities, risks, and safety of advanced AI systems, mandated by the AI Safety Summit.",
          published_date="2025-01-29", arxiv_url="https://arxiv.org/abs/2501.17805",
          pdf_url="https://arxiv.org/pdf/2501.17805", is_classic=True, source="seed"),

    Paper(arxiv_id="2407.21783", title="The Llama 3 Herd of Models",
          authors='["Meta AI"]',
          abstract="Technical report on Llama 3, a herd of open-source foundation models supporting multilinguality, coding, reasoning, and tool usage with safety evaluations.",
          published_date="2024-07-31", arxiv_url="https://arxiv.org/abs/2407.21783",
          pdf_url="https://arxiv.org/pdf/2407.21783", is_classic=True, source="seed"),

    Paper(arxiv_id="2404.01399", title="Developing Safe and Responsible Large Language Models -- A Comprehensive Framework",
          authors='["Shaina Raza", "Oluwanifemi Bamgbose", "Shardul Ghuge", "Fatemeh Tavakoli"]',
          abstract="Comprehensive framework for developing safe and responsible LLMs covering the full development lifecycle.",
          published_date="2024-04-01", arxiv_url="https://arxiv.org/abs/2404.01399",
          pdf_url="https://arxiv.org/pdf/2404.01399", is_classic=True, source="seed"),

    Paper(arxiv_id="2410.18114", title="Bridging Today and the Future of Humanity: AI Safety in 2024 and Beyond",
          authors='["Hao Sun"]',
          abstract="Broad perspective on AI safety emphasizing that current efforts should anticipate potential risks in the expanding AI landscape.",
          published_date="2024-10-23", arxiv_url="https://arxiv.org/abs/2410.18114",
          pdf_url="https://arxiv.org/pdf/2410.18114", is_classic=True, source="seed"),

    Paper(arxiv_id="2403.04893", title="A Safe Harbor for AI Evaluation and Red Teaming",
          authors='["Shayne Longpre", "Sayash Kapoor", "Kevin Klyman", "Ashwin Ramaswami", "Rishi Bommasani", "Boaz Barak", "Arvind Narayanan", "Percy Liang"]',
          abstract="Proposes legal and institutional safe harbors to enable independent AI safety evaluation and red teaming without legal risk.",
          published_date="2024-03-07", arxiv_url="https://arxiv.org/abs/2403.04893",
          pdf_url="https://arxiv.org/pdf/2403.04893", is_classic=True, source="seed"),

    Paper(arxiv_id="2411.11296", title="Steering Language Model Refusal with Sparse Autoencoders",
          authors='["Kyle O\'Brien", "David Majercak"]',
          abstract="Uses sparse autoencoders to identify and steer refusal-related features in language models for more precise safety control.",
          published_date="2024-11-18", arxiv_url="https://arxiv.org/abs/2411.11296",
          pdf_url="https://arxiv.org/pdf/2411.11296", is_classic=True, source="seed"),

    Paper(arxiv_id="2410.19278", title="Applying Sparse Autoencoders to Unlearn Knowledge in Language Models",
          authors='["Eoin Ó Catháin", "Aaquib Syed"]',
          abstract="Explores using sparse autoencoders to selectively unlearn specific knowledge from language models for safety purposes.",
          published_date="2024-10-25", arxiv_url="https://arxiv.org/abs/2410.19278",
          pdf_url="https://arxiv.org/pdf/2410.19278", is_classic=True, source="seed"),

    Paper(arxiv_id="2403.05812", title="Algorithmic Progress in Language Models",
          authors='["Anson Ho", "Tamay Besiroglu", "Ege Erdil", "David Owen", "Robi Rahman", "Zifan Carl Guo", "David Atkinson", "Neil Thompson", "Jaime Sevilla"]',
          abstract="Quantifies algorithmic progress in language models, finding that effective compute doubles roughly every 8 months.",
          published_date="2024-03-08", arxiv_url="https://arxiv.org/abs/2403.05812",
          pdf_url="https://arxiv.org/pdf/2403.05812", is_classic=True, source="seed"),

    Paper(arxiv_id="2502.09288", title="AI Safety for Everyone",
          authors='["Fang Liu", "Xiaoyu Shen"]',
          abstract="Surveys AI safety challenges across the full AI lifecycle, making safety concepts accessible to a broad audience.",
          published_date="2025-02-13", arxiv_url="https://arxiv.org/abs/2502.09288",
          pdf_url="https://arxiv.org/pdf/2502.09288", is_classic=True, source="seed"),

    Paper(arxiv_id="2407.18369", title="AI Safety in Generative AI Large Language Models: A Survey",
          authors='["Jaymari Chua", "Yun Li", "Feng Xia"]',
          abstract="Surveys safety challenges specific to generative AI and LLMs, covering alignment techniques, robustness, and deployment risks.",
          published_date="2024-07-25", arxiv_url="https://arxiv.org/abs/2407.18369",
          pdf_url="https://arxiv.org/pdf/2407.18369", is_classic=True, source="seed"),

    Paper(arxiv_id="2412.09751", title="AI Red-teaming is a Sociotechnical Problem: On Values, Labor, and Harms",
          authors='["Inioluwa Deborah Raji", "Renée Shelby", "Andrew Smart", "Edgar Ross Owen"]',
          abstract="Examines AI red-teaming as a sociotechnical practice, analyzing its values, labor dynamics, and potential harms to red teamers.",
          published_date="2024-12-13", arxiv_url="https://arxiv.org/abs/2412.09751",
          pdf_url="https://arxiv.org/pdf/2412.09751", is_classic=True, source="seed"),
]


async def seed_database() -> int:
    """Insert all seed papers into the database. Returns count of papers inserted."""
    count = 0
    for paper in SEED_PAPERS:
        paper_id = await repo.upsert_paper(paper)
        if paper_id:
            count += 1
    return count
