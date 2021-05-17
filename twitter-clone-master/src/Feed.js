import React, { useState, useEffect } from "react";
import TweetBox from "./TweetBox";
import Post from "./Post";
import "./Feed.css";
import axios from "axios";
import { Button } from "@material-ui/core";
import FlipMove from "react-flip-move";

function Feed() {
  const [posts, setPosts] = useState([]);
  const [predictMessage, setPredictMessage] = useState("");

  useEffect(() => {
    fetch('/api').then(response => response.json().then(data => {
      setPosts(data);
      console.log(data);
    })
   );
  }, []);

  useEffect(() => {
    fetch('/api-quotes').then(response => response.json()
    .then(data => {
      setPredictMessage(data[0].text);
      console.log(data);
    })
   );
  }, []);
  
  return (
    <div className="feed">
      <div className="feed__header">
        <h2>Home</h2>
      </div>

      <TweetBox />

      <div className="generate__header">
      <form method="post">
        <center><h2 style={{fontSize:"20px",fontWeight:"800",paddingBottom:"15px"}}>Let's Go!</h2>
        <p style={{color:"gray"}}>Click on the button below to create AI-generated text.</p>
        <Button
          onClick={() => {
            axios.post('/api-quotes', {
              text: predictMessage
            })
          }}
          className="tweetBox__tweetButton"
          type="submit"
          >
          Generate
        </Button>
        <input 
          value={predictMessage} 
          placeholder="" 
          className="predict" 
          type="predict" 
          name="predict" 
          readonly /><br></br>
          <Button
          onClick={() => {
            axios.post('/api', {
              displayName: "Bob Choi",
              username: "alychoi123",
              verified: 1,
              text: predictMessage,
              image: "https://64.media.tumblr.com/avatar_f8d55dc74283_128.pnj",
              avatar:
              "https://static.wikia.nocookie.net/character-stats-and-profiles/images/d/d3/EKTwbfMUEAgrwTc.jpg/revision/latest?cb=20200612053140"
            }).then(response => response.json())
            .then(data => setPredictMessage(data.text))
            .catch(function (error) {
              console.log(error);
            });
          }}
          className="tweetBox__tweetButton"
          type="submit"
          >
          Tweet
        </Button>
        </center>
        </form>
      </div>

      <FlipMove>
        {posts.map((post) => (
          <Post
            id={post.id}
            key={post.text}
            displayName={post.displayName}
            username={post.username}
            verified={post.verified}
            text={post.text}
            avatar={post.avatar}
            image={post.image}
          />
        ))}
      </FlipMove>
    </div>
  );
}

export default Feed;
