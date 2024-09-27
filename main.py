import subprocess

def main():
    with open('deyappify_input.txt', 'r') as file:
        arguments = [line.strip() for line in file]

    username = arguments[0]
    password = arguments[1]
    fst_week = arguments[2]
    lst_week = arguments[3]
    your_api = arguments[4]
    extra_prompt = arguments[5]






    subprocess.run(['python', 'get_links.py',fst_week,lst_week])
    subprocess.run(['python','process_lectures.py'])
    subprocess.run(['python','process_pdfs.py'])
    subprocess.run(['python', 'work_with_LLM.py', your_api, extra_prompt])


if __name__ == "__main__":
    main()

