import requests
import streamlit as st
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
from streamlit_chat import message

st.header('Hangman')

if 'generated_responses' not in st.session_state:
    st.session_state['generated_responses'] = []

if 'user_inputs' not in st.session_state:
    st.session_state['user_inputs'] = []

if 'psid' not in st.session_state:
    st.session_state['psid'] = ''

if 'psidts' not in st.session_state:
    st.session_state['psidts'] = ''

if 'psidcc' not in st.session_state:
    st.session_state['psidcc'] = ''

if 'hangman_started' not in st.session_state:
    st.session_state['hangman_started'] = False

st.session_state['psid'] = st.text_input('1PSID: ', st.session_state['psid'], type='password')
st.session_state['psidts'] = st.text_input('1PSIDTS: ', st.session_state['psidts'], type='password')
st.session_state['psidcc'] = st.text_input('1PSIDCC: ', st.session_state['psidcc'], type='password')

session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID", st.session_state.psid)
session.cookies.set("__Secure-1PSIDTS", st.session_state.psidts)
session.cookies.set("__Secure-1PSIDCC", st.session_state.psidcc)

def query(payload):
    bard = Bard(token=st.session_state.psid, session=session)
    response = bard.get_answer(payload)
    return response

if st.session_state.hangman_started == False and st.session_state.psid and st.session_state.psidts and st.session_state.psidcc:
    output = query('Let\'s play Hangman')
    message('Are you ready to play Hangman?')
    st.session_state['hangman_started'] = True

with st.form('form', clear_on_submit = True):
    user_input = st.text_input('Message: ', '')
    submitted = st.form_submit_button('Send')

if submitted and user_input:
    output = query(user_input)

    st.session_state.user_inputs.append(user_input)
    st.session_state.generated_responses.append(output['content'])

if st.session_state['generated_responses']:
    for i in range(0, len(st.session_state['generated_responses']), 1):
        message(st.session_state['user_inputs'][i], is_user = True, key=str(i) + '_user')
        message(st.session_state['generated_responses'][i], key=str(i))


