# ImageBiTe: A Bias Tester framework for T2I Models

ImageBiTe is a framework for testing representational harms in text-to-image (T2I) models. Given an ethical requirements model, ImageBiTe prompts a T2I model and evaluates the output in order to detect stereotyping, under-representation, ex-nomination and denigration of protected groups. It includes a library of prompts to test sexism, racism, ageism, and discrimination with regard to physical impairments. Any contributor is welcome to add new ethical concerns to assess and their prompt templates.

## Code Repository Structure

The following tree shows the list of the repository's sections and their main contents:

```
└── imagebite                               // The source code of the package.
      ├── imagebite.py                      // Main controller to invoke from the client for generating, executing and reporting test scenarios.
      └── resources
             ├── factories.json             // Endpoints for invoking and testing online T2I models.
             ├── generic_validators.json    // Prompts for generic, qualitative evaluation of generated images.
             └── prompts_t2i_CO_RE.csv      // The prompt templates libraries in CSV format.
```

## Requirements

- huggingface-hub 0.26.1
- numpy 2.1.2
- openai 1.52.1
- pandas 2.2.3
- pillow 11.0.0
- python-dotenv 1.0.1
- PyGithub 2.4.0
- requests 2.32.3

Your project needs the following keys in the .env file:

- API_KEY_OPENAI, to properly connect to OpenAI's API and models.
- API_KEY_HUGGINGFACE, to properly invoke Inference APIs in HuggingFace.
- API_KEY_REPLICATE, to properly connect to models hosted on Replicate.
- GITHUB_REPO, the name of the public repository where to upload generated images.
- GITHUB_REPO_PREFIX, the URL of the public repository where to upload generated images.
- GITHUB_TOKEN, to properly connect to the GitHub repository.

## Governance and Contribution

The development and community management of this project follows the governance rules described in the [GOVERNANCE.md](GOVERNANCE.md) document.

At SOM Research Lab we are dedicated to creating and maintaining welcoming, inclusive, safe, and harassment-free development spaces. Anyone participating will be subject to and agrees to sign on to our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

This project is part of a research line of the [SOM Research Lab](https://som-research.uoc.edu/), but we are open to contributions from the community. Any comment is more than welcome! If you are interested in contributing to this project, please read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Publications

Related publications:

> Sergio Morales, Robert Clarisó and Jordi Cabot. "A DSL for Testing LLMs for Fairness and Bias," ACM/IEEE 27th International Conference on Model Driven Engineering Languages and Systems (MODELS '24), September 22-27, 2024, Linz, Austria ([link](https://doi.org/10.1145/3640310.3674093))

> Sergio Morales, Robert Clarisó and Jordi Cabot. "Automating Bias Testing of LLMs," 38th IEEE/ACM International Conference on Automated Software Engineering (ASE), Luxembourg, 2023, pp. 1705-1707 ([link](https://doi.org/10.1109/ASE56229.2023.00018))

> Sergio Morales, Robert Clarisó and Jordi Cabot. "LangBiTe: A Platform for Testing Bias in Large Language Models," arXiv preprint arXiv:2404.18558 (2024) [cs.SE] ([link](https://doi.org/10.48550/arXiv.2404.18558))

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The source code for the site is licensed under the MIT License, which you can find in the LICENSE.md file.
