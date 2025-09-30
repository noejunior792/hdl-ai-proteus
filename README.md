# ALU AI Proteus

ALU AI Proteus is a powerful tool that leverages artificial intelligence to generate hardware description language (HDL) code from natural language prompts. It automates the entire process from design to simulation-ready project files for Proteus. This project is ideal for students, hobbyists, and engineers who want to quickly prototype and test digital logic designs.

## Features

-   **Natural Language to HDL:** Describe your circuit in plain English and get VHDL or Verilog code.
-   **AI-Powered:** Uses Azure OpenAI to understand your requirements and generate the code.
-   **Automatic Compilation:** Compiles the generated HDL code using GHDL for VHDL and Icarus Verilog for Verilog.
-   **Proteus Integration:** Exports the compiled design into a Proteus project file (`.pdsprj`), ready for simulation.
-   **Cross-Platform:** While designed on Linux, it generates Proteus projects for use on Windows.

## Workflow

1.  **Prompt:** You provide a natural language prompt describing the circuit you want to create.
2.  **Generate:** The tool sends the prompt to Azure OpenAI, which generates the corresponding VHDL or Verilog code.
3.  **Save:** The generated code is saved in the `generated/` directory.
4.  **Compile:** The tool automatically compiles the generated code and places the artifacts in the `build/` directory.
5.  **Export:** Finally, it creates a Proteus project file (`.pdsprj`) in the `export/` directory.

## Installation

### Prerequisites

-   Python 3.x
-   pip (Python package installer)
-   GHDL (for VHDL compilation)
-   Icarus Verilog (for Verilog compilation)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd alu-ai-proteus
    ```

2.  **Install dependencies:**
    The script can automatically install the required dependencies on Debian-based Linux distributions (like Ubuntu). When you run the script for the first time, it will ask you if you want to install them.

    If you prefer to install them manually, you can use the following commands:

    ```bash
    # For Debian/Ubuntu
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y python3 python3-pip ghdl iverilog

    # Install Python packages
    pip3 install -r requirements.txt
    ```

## Usage

1.  **Run the main script:**
    ```bash
    python3 src/main.py
    ```

2.  **Follow the prompts:**
    -   The script will first ask if you want to install the dependencies.
    -   Then, it will ask you to enter your natural language prompt. You can enter multi-line prompts. Press `Ctrl+D` on a new line to finish.
    -   Finally, provide a name for your circuit (without spaces).

### Example

```
$ python3 src/main.py
Do you want to install required dependencies (Python3, pip, GHDL, Icarus Verilog, requests)? (y/n) n
Enter the natural language prompt (press Ctrl+D on a new line to end):
Create a 4-bit ALU in VHDL with the following operations: 000: A + B, 001: A - B, 010: A AND B, 011: A OR B, 100: A XOR B, 101: NOT A, 110: Left shift A by 1, 111: Output constant 1111. Inputs: A[3:0], B[3:0], Sel[2:0]. Output: Result[3:0]. Make sure to use a process block and a case statement for Sel.
Enter a name for the circuit (no spaces): my_alu
Prompt sent: Create a 4-bit ALU in VHDL...

Code received from AI.
Code saved to generated/my_alu.vhdl
Starting compilation...
Compilation successful.
Exporting to .pdsprj...
Export successful.
```

After running the script, you will find `my_alu.pdsprj` in the `export/` directory. You can then transfer this file to a Windows machine with Proteus to open and simulate the circuit.

## Project Structure

```
.
├── .env                # Environment variables for API keys
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── build/              # Compiled artifacts
├── export/             # Exported Proteus projects
├── generated/          # Generated HDL files
└── src/                # Source code
    ├── main.py         # Main script to run the application
    ├── azure_api.py    # Handles communication with Azure OpenAI
    ├── compiler.py     # Handles HDL compilation
    └── exporter.py     # Handles exporting to Proteus project format
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.