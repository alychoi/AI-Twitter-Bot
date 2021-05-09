import React, { useState } from "react";
import "./TweetBox.css";
import { Avatar, Button } from "@material-ui/core";

function TweetBox() {
  const [tweetMessage, setTweetMessage] = useState("");
  const [tweetImage, setTweetImage] = useState("");

  /*const sendTweet = async () => {
    //e.preventDefault();

    const response = await fetch('/api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        displayName: "Bob Choi",
        username: "alychoi123",
        verified: true,
        text: tweetMessage,
        image: tweetImage,
        avatar:
         "https://i.pinimg.com/736x/fd/a1/3b/fda13b9d6d88f25a9d968901d319216a.jpg"
      })
    });

      if (response.ok) {
        console.log("It worked!");
      }
    }*/
    /*.then(response => response.json()).then(json => {
      const accessToken = json.access_token;
      setTweetMessage(accessToken);
      setTweetImage(accessToken);
      //setTweetMessage(json);
      //setTweetImage(json);
      console.log(json);
    });*/

    /*db.collection("posts").add({
      displayName: "Bob Choi",
      username: "alychoi123",
      verified: true,
      text: tweetMessage,
      image: tweetImage,
      avatar:
        "https://i.pinimg.com/736x/fd/a1/3b/fda13b9d6d88f25a9d968901d319216a.jpg",
    });

    setTweetMessage("");
    setTweetImage("");

    console.log(setTweetMessage);
  };*/

  return (
    <div className="tweetBox">
      <form>
        <div className="tweetBox__input">
          <Avatar src="https://i.pinimg.com/736x/fd/a1/3b/fda13b9d6d88f25a9d968901d319216a.jpg" />
          <input
            onChange={(e) => setTweetMessage(e.target.value)}
            value={tweetMessage}
            placeholder="What's happening?"
            type="text"
          />
        </div>
        <input
          value={tweetImage}
          onChange={(e) => setTweetImage(e.target.value)}
          className="tweetBox__imageInput"
          placeholder="Optional: Enter image URL"
          type="text"
        />

        <Button
          onClick={async () => {
            const response = await fetch('/api', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                displayName: "Bob Choi",
                username: "alychoi123",
                verified: true,
                text: tweetMessage,
                image: tweetImage,
                avatar:
                "https://i.pinimg.com/736x/fd/a1/3b/fda13b9d6d88f25a9d968901d319216a.jpg"
              })
            });

            if (response.ok) {
              console.log("It worked!");
              setTweetMessage("");
              setTweetImage("");
            }
          }}
          type="submit"
          className="tweetBox__tweetButton"
        >
          Tweet
        </Button>
      </form>
    </div>
  );
}

export default TweetBox;
