import React, { forwardRef, useState, useEffect } from "react";
import VerifiedUserIcon from "@material-ui/icons/VerifiedUser";
import Post from "./Feed";
import "./Comments.css";
import { Avatar, Button } from "@material-ui/core";
import db from "./firebase";
import FlipMove from "react-flip-move";

const PostComment = forwardRef(
    ({ displayName, username, verified, text, avatar }, ref) => {
      return (
        <div className="post" ref={ref}>
          <div className="post__avatar">
            <Avatar src={avatar} />
          </div>
          <div className="post__body">
            <div className="post__header">
              <div className="post__headerText">
                <h3>
                  {displayName}{" "}
                  <span className="post__headerSpecial">
                    {verified && <VerifiedUserIcon className="post__badge" />} @
                    {username}
                  </span>
                </h3>
              </div>
              <div className="post__headerDescription">
                <p>{text}</p>
              </div>
            </div> 
        </div>
        </div>
        );
    }
  ); 


function Comments() {
    const [tweetComment, setTweetComment] = useState("");
    const [comments, setComments] = useState([]);

    useEffect(() => {
      db.collection("comments").onSnapshot((snapshot) =>
        setComments(snapshot.docs.map((doc) => doc.data()))
      );
    }, []);

  const sendComment = (e) => {
    e.preventDefault();

    db.collection("comments").add({
      displayName: "Bob",
      username: "bob",
      verified: false,
      text: tweetComment,
      avatar:
        "https://yt3.ggpht.com/ytc/AAUvwnhkZjfj3AhZNOvbxzIzVLTKZZHGLAlIHVstuYx1=s900-c-k-c0x00ffffff-no-rj",
    });

    setTweetComment("");
  };
  const idMatches = true;

  return (
    <div className="tweetBox">
        <form>
            <div className="tweetBox__input">
            <Avatar src="https://yt3.ggpht.com/ytc/AAUvwnhkZjfj3AhZNOvbxzIzVLTKZZHGLAlIHVstuYx1=s900-c-k-c0x00ffffff-no-rj" />
            <input
                onChange={(e) => setTweetComment(e.target.value)}
                value={tweetComment}
                placeholder="Reply..."
                type="text"
            />
            </div>
            <Button
            onClick={sendComment}
            type="submit"
            className="tweetBox__tweetButton"
            >
            Reply
            </Button>
            { idMatches &&
            <FlipMove>
        {comments.map((comment) => (
          <PostComment
            id={comment.id}
            key={comment.text}
            displayName={comment.displayName}
            username={comment.username}
            verified={comment.verified}
            text={comment.text}
            avatar={comment.avatar}
          />
        ))}
      </FlipMove>}
        </form>
    </div>
  );
}

export default Comments;
