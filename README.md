
# termo 
- Terminal Macros

**termo** is a command-line tool designed to help users record and run macros directly from the terminal. This tool allows you to capture a sequence of commands, store them under a specific name, and then replay those commands as needed. It's particularly useful for automating repetitive tasks.

### Features

- **Record Macros**: Capture a series of commands under a specific name.
- **Run Macros**: Replay the commands in a recorded macro with a single command.
- **Simple CLI Interface**: Easily start, abort, finish, and run macros with straightforward commands.

### Requirements

- Python 3.12+
- `click` package (handled automatically during installation)

### Installation

To install **termo** using `pip`:

1. Clone the repository:
   ```bash
   git clone https://github.com/ajaypremshankar/homebrew-termo.git
   cd homebrew-termo
   ```

2. Install with `pip`:
   ```bash
   pip install .
   ```

Or you can install it directly from [Homebrew](https://brew.sh/) if it's published:

```bash
brew install ajaypremshankar/homebrew-termo/termo
```

### Usage

Once installed, the `macro` command will be available in your terminal. Here’s how to use it:

#### 1. Start Recording a Macro

To start recording a macro, use:

```bash
tm new <name>
```

Replace `<name>` with the name you’d like to give to this macro.

Example:
```bash
tm new my_macro
```

#### 2. Abort Recording

If you want to stop recording without saving, use:

```bash
tm cancel
```

This will discard all commands recorded since the last `record start`.

#### 3. Finish Recording

To stop recording and save the commands to the macro, use:

```bash
tm save
```

The commands recorded between `record start` and `record finish` will be saved.

#### 4. Run a Macro

To replay the commands stored in a macro, use:

```bash
macro exe <name>
```

Replace `<name>` with the name of the macro you want to run.

Example:
```bash
macro exe my_macro
```

### Example Workflow

1. Start recording a macro named `backup`:
   ```bash
   tm new backup
   ```

2. Run the commands you want to record, for example:
   ```bash
   cp ~/Documents/important-file.txt ~/Backups/
   echo "Backup completed"
   ```

3. Finish recording the macro:
   ```bash
   tm save
   ```

4. Now, whenever you want to execute the `backup` macro, simply run:
   ```bash
   macro exe backup
   ```


### Discover all the supported commands:

```bash
tm --help
```

### Uninstalling

To uninstall **termo**, you can use `pip`:

```bash
pip uninstall termo
```

Or if installed via Homebrew:

```bash
brew uninstall termo
```

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
