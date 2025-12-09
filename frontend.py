import streamlit
from conversation_agent import ConversationAgent 
from vision_agent import VisionAgent
from config import LLM_MODELS
import base64


if "conversation_agent" not in streamlit.session_state :
	streamlit.session_state.conversation_agent = ConversationAgent()

if "vision_agent" not in streamlit.session_state:
	streamlit.session_state.vision_agent = VisionAgent()



def init_header():
	streamlit.set_page_config(page_title="Jarvis", page_icon="🤖")
	streamlit.title("🤖 Jarvis ton baron préféré !")
	streamlit.write("Il est un peu enervé, fais attention à ce que tu racontes...")



def show_discussion_history(history_placeholder):
	container = history_placeholder.container()
	with container:
		for message in streamlit.session_state.conversation_agent.history:
			if message["role"] != "system":
				with streamlit.chat_message(message["role"]):
					streamlit.write(message["content"])





def streamlit_file_object_to_base64(file_object):
    bytes_data = file_object.read()
    b64_bytes = base64.b64encode(bytes_data)
    b64_str = b64_bytes.decode("utf-8")
    mime = "image/png" if file_object.type == "image/png" else "image/jpeg"
    return f"data:{mime};base64,{b64_str}"


def user_interface():
	init_header()
	history_placeholder = streamlit.empty() 
	show_discussion_history(history_placeholder)
	with streamlit.container():
		
		user_input = streamlit.chat_input("N'oublie pas à qui tu parle !")
		uploaded_file = streamlit.file_uploader(
						"📎 Chargez une Image",
						type=["png", "jpg", "jpeg"],               # Autoriser tous les types ; précisez si besoin
						accept_multiple_files=False,
						key="file_uploader",
				)
		_, col2 = streamlit.columns([2, 1])
		with col2:
			streamlit.empty()
			selected_model = streamlit.selectbox("Choisis ton modèle gamin...", LLM_MODELS)

		if user_input:
			if uploaded_file:
				image_b64 = streamlit_file_object_to_base64(file_object=uploaded_file)
				response = streamlit.session_state.vision_agent.ask_vision_model(
					user_interaction=user_input,
					image_b64 = image_b64
					)
				print(response)
			else:
				streamlit.session_state.conversation_agent.ask_llm(user_interaction=user_input, model=selected_model)
				show_discussion_history(history_placeholder)



if __name__ == "__main__":
	user_interface()
