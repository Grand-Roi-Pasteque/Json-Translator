import json
import tkinter as tk

def compare_json_files(model_file, translation_file):
    with open(model_file, 'r', encoding='utf-8') as file1, open(translation_file, 'r+', encoding='utf-8') as file2:
        model_data = json.load(file1)
        translation_data = json.load(file2)
        
        missing_keys = [key for key in model_data if key not in translation_data]
        extra_keys = [key for key in translation_data if key not in model_data]
        
        for key in extra_keys:
            del translation_data[key]
        
        def submit():
            nonlocal current_key_index
            key = missing_keys[current_key_index]
            value = entry.get("1.0", tk.END).strip()
            
            if value:
                translation_data[key] = value
                
                if current_key_index < len(missing_keys) - 1:
                    entry.insert(tk.END, ',\n')
                
                file2.seek(0)
                json.dump(translation_data, file2, indent=4, ensure_ascii=False)
                file2.truncate()
            
            current_key_index += 1
            if current_key_index < len(missing_keys):
                show_next_key()
            else:
                root.quit()

        def show_next_key():
            key = missing_keys[current_key_index]
            entry.delete("1.0", tk.END)
            entry.insert(tk.END, "")
            label.config(text=f"Missing Translation:\n\nKey: {key}\nValue: {model_data[key]}")

        root = tk.Tk()
        root.title("Translation Editor")
        root.iconbitmap('icon.ico')
        root['bg']='#2f2f2f'
        
        label = tk.Label(root, text="")
        label.pack()
        
        entry = tk.Text(root, height=10, width=50)
        entry.pack()
        
        submit_button = tk.Button(root, text="Submit", command=submit)
        submit_button.pack()
        
        current_key_index = 0
        show_next_key()
        
        root.protocol("WM_DELETE_WINDOW", root.quit)
        root.mainloop()
        root.destroy()
        
        print("Translation updates have been saved.")
    
    file2.close()

# Place the file you want to translate in the input folder and change the "model_file_path" value below to the path of your input file.
model_file_path = 'input/'

# Place the output file in the output folder and change the "translation_file_path" value below to the path of your output file.
translation_file_path = 'output/'


compare_json_files(model_file_path, translation_file_path)
