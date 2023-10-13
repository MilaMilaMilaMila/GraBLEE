import py4cytoscape as p4c
import os
import multiprocessing
import requests.exceptions


def open_cytoscape_session(session_filepath=None):
    p4c.open_session(file_location=session_filepath)


def close_cytoscape_session(save_changes=False, changed_session_name=None):
    p4c.close_session(save_before_closing=save_changes, filename=changed_session_name)


def run_cytoscape():
    os.system('run_cs_cmd.py')


# function check - is cytoscape opened
# If not - cytoscape will be opened
def show_session_in_cytoscape(session_filepath=None, save_changes=False, changed_session_name=None):
    if __name__ == '__main__':
        try:
            p4c.cytoscape_ping()
        except requests.exceptions.RequestException:
            process1 = multiprocessing.Process(target=run_cytoscape)
            process1.start()

        flag = 1
        while flag:
            try:
                flag = 0
                p4c.cytoscape_ping()
            except requests.exceptions.RequestException:
                flag = 1

        open_cytoscape_session(session_filepath=session_filepath)
        # code for keeping cytoscape opened
        print('Please, input any not empty string to close session:')
        stop_signal = input()

        close_cytoscape_session(save_changes=save_changes, changed_session_name=changed_session_name)


# example
show_session_in_cytoscape("main_test_session.cys", save_changes=False)
show_session_in_cytoscape("main_test_session.cys", save_changes=True)
show_session_in_cytoscape("main_test_session.cys", save_changes=True, changed_session_name="changed_test_main_session")

