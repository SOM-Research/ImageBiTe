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
- GITHUB_REPO, the name of the public repository where to upload generated images.
- GITHUB_REPO_PREFIX, the URL of the public repository where to upload generated images.
- GITHUB_TOKEN, to properly connect to the GitHub repository.

## Governance and Contribution

The development and community management of this project follows the governance rules described in the [GOVERNANCE.md](GOVERNANCE.md) document.

At SOM Research Lab we are dedicated to creating and maintaining welcoming, inclusive, safe, and harassment-free development spaces. Anyone participating will be subject to and agrees to sign on to our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

This project is part of a research line of the [SOM Research Lab](https://som-research.uoc.edu/), but we are open to contributions from the community. Any comment is more than welcome! If you are interested in contributing to this project, please read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Publications

Related publications:

> Sergio Morales, Robert Clarisó and Jordi Cabot, "ImageBiTe: A Framework for Evaluating Representational Harms in Text-to-Image Models," 2025 IEEE/ACM 4th International Conference on AI Engineering – Software Engineering for AI (CAIN), Ottawa, ON, Canada, 2025, pp. 95-106, doi: [10.1109/CAIN66642.2025.00019](https://doi.org/10.1109/CAIN66642.2025.00019).

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The source code for the site is licensed under the MIT License, which you can find in the LICENSE.md file.
