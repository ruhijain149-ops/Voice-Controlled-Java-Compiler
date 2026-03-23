
import speech_recognition as sr
import subprocess
import os

def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        heard = r.recognize_google(audio)
        print(f"You said: {heard}")
        return heard.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def compile_and_run_java(java_file_path):
    try:
        java_dir = os.path.dirname(java_file_path)
        java_filename = os.path.basename(java_file_path)
        class_name = os.path.splitext(java_filename)[0]
        print(f"Compiling {java_filename}...")
        compile_result = subprocess.run(
            ['/usr/bin/javac', java_file_path],
            capture_output=True,
            text=True,
            cwd=java_dir or '.'
        )
        if compile_result.returncode != 0:
            print("Compilation failed:")
            print(compile_result.stderr)
            return False
        print("Compilation successful.")
        print(f"Running {class_name}...")
        run_result = subprocess.run(
            ['/usr/bin/java', class_name],
            capture_output=True,
            text=True,
            cwd=java_dir or '.'
        )
        if run_result.returncode != 0:
            print("Execution failed:")
            print(run_result.stderr)
            return False
        print("Execution successful:")
        print(run_result.stdout)
        return True
    except FileNotFoundError:
        print("Java compiler (javac) or Java Runtime (java) not found. Ensure Java is installed and configured in your PATH.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    java_code = """
public class PatternStar {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 1; i <= n; i++) {
            for (int j = i; j < n; j++)
                System.out.print(" ");
            for (int j = 1; j <= (2 * i - 1); j++)
                System.out.print("*");
            System.out.println();
        }
        for (int i = n - 1; i >= 1; i--) {
            for (int j = n; j > i; j--)
                System.out.print(" ");
            for (int j = 1; j <= (2 * i - 1); j++)
                System.out.print("*");
            System.out.println();
        }
    }
}
"""
    with open("PatternStar.java", "w", encoding="utf-8") as f:
        f.write(java_code)
    print("Voice-controlled Java runner ready.")
    print("Say 'compile and run java' to execute, or 'exit' to quit.\n")
    while True:
        user_command = listen_for_command()
        if "compile and run java" in user_command:
            print("Attempting to compile and run Java...")
            compile_and_run_java("PatternStar.java")
        elif "exit" in user_command or "quit" in user_command:
            print("Exiting program.")
            break
        else:
            print("Command not recognized. Try saying 'compile and run java' or 'exit'.")





