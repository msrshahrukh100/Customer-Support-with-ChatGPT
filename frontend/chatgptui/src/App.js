import React, { useState } from 'react';
import './Chat.css';
import ChatGPTImage from './images/chatgpt.svg';
import UserImage from './images/user.svg'
import axios from 'axios';


const Chat = () => {
  const ts = new Date();
  const defaultMessages = [
    {
      sender: "ChatGPT",
      msg: "Hi! How can I help you today?",
      ts: `${ts.getHours()}:${ts.getMinutes()}`
    },

  ]
  const [messages, setMessages] = useState(defaultMessages);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setNewMessage(e.target.value);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim() === '') return;
    setLoading(true);
    let ts = new Date();
    let newMessages = [...messages, {
      sender: "Shahrukh",
      msg: newMessage,
      ts: `${ts.getHours()}:${ts.getMinutes()}`,
    }]
    setMessages(newMessages);

    axios.get(`http://localhost:8000/ask?q=${encodeURIComponent(newMessage)}`)
      .then(function (response) {
        ts = new Date();
        setMessages([...newMessages, {
          sender: "ChatGPT",
          msg: response.data.text,
          ts: `${ts.getHours()}:${ts.getMinutes()}`,
        }])
        setNewMessage("");
        setLoading(false);
      })
      .catch(function (error) {
        console.log(error);
      });

  };

  return (
    <section className="msger">
      <header className="msger-header">
        <div className="msger-header-title">
          <i className="fas fa-comment-alt"></i> Amazon Customer Support
        </div>
        <div className="msger-header-options">
          <span><i className="fas fa-cog"></i></span>
        </div>
      </header>

      <main className="msger-chat">

        {messages.map((item, index) => (
          <div key={`message-${index}`} className={item.sender === "ChatGPT" ? "msg left-msg" : "msg right-msg"}>
            <div
              className="msg-img"
              style={{ backgroundImage: `url(${item.sender === "ChatGPT" ? ChatGPTImage : UserImage})` }}></div>

            <div className="msg-bubble">
              <div className="msg-info">
                <div className="msg-info-name">{item.sender}</div>
                <div className="msg-info-time">{item.ts}</div>
              </div>
              <div className="msg-text">
                {item.msg}
              </div>
            </div>
          </div>
        ))}

      </main>

      <form className="msger-inputarea">
        <input value={newMessage} onChange={e => setNewMessage(e.target.value)} type="text" className="msger-input" placeholder="Enter your message..." />
        <button disabled={loading} className="msger-send-btn" onClick={handleSendMessage}>Send</button>
      </form>
    </section>
  );
};

export default Chat;
