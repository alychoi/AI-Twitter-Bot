import React, { useState, useEffect } from "react";
import TweetBox from "./TweetBox";
import Post from "./Post";
import "./Feed.css";
import FlipMove from "react-flip-move";

function Feed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch('/api').then(response => response.json().then(data => {
      setPosts(data);
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
        <input type="submit"
          //onClick={sendTweet}
          type="submit"
          className="tweetBox__tweetButton"
          value="Generate"
        /></center>
        <input type="predict" name="predict"/>
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
