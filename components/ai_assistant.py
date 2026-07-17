import streamlit as st
from utils.chatbot import get_chat_response

st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
def show_ai_assistant(context):

    st.markdown("---")

    st.markdown("""
    <h2 style="
    color:white;
    font-size:36px;
    font-weight:700;
    margin-bottom:10px;
    ">
    🤖 Ask MediSense AI
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:white;
    font-size:17px;
    margin-bottom:20px;
    opacity:0.9;
    ">
    Ask anything about your prediction, report, symptoms, diet or lifestyle.
    </p>
    """, unsafe_allow_html=True)

    if "assistant_messages" not in st.session_state:
        st.session_state.assistant_messages = []

    for msg in st.session_state.assistant_messages:

        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.markdown(
                    f"""
                    <div style="color:white; line-height:1.7; font-size:16px;">
                        {msg["content"].replace(chr(10), "<br>")}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(msg["content"])

    prompt = st.chat_input("Ask a follow-up question...")

    if prompt:

        st.session_state.assistant_messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        history = ""

        for m in st.session_state.assistant_messages:
            history += f"{m['role']}: {m['content']}\n"

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = get_chat_response(
                    context,
                    history
                )

            st.markdown(
                f"""
                <div style="color:white; line-height:1.7; font-size:16px;">
                    {answer.replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.session_state.assistant_messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    if st.button("🗑 Clear Conversation"):

        st.session_state.assistant_messages = []

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)