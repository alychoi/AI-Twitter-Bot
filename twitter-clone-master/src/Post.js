import React, { forwardRef, useState } from "react";
import { Button } from "@material-ui/core";
import "./Post.css";
import { Avatar } from "@material-ui/core";
import VerifiedUserIcon from "@material-ui/icons/VerifiedUser";
import ChatBubbleOutlineIcon from "@material-ui/icons/ChatBubbleOutline";
import RepeatIcon from "@material-ui/icons/Repeat";
import FavoriteBorderIcon from "@material-ui/icons/FavoriteBorder";
import PublishIcon from "@material-ui/icons/Publish";
import Comments from "./Comments";


const Post = forwardRef(
  ({ id, displayName, username, verified, text, image, avatar }, ref) => {
    const [visible, setVisible] = useState(false);

    function hideMe() {
      setVisible(false);
    }

    function showMe() {
      setVisible(true);
    }

    let style = {
      position: "fixed",
      zIndex: "1",
      paddingTop: "300px",
      width: "50%",
      height: "100%",
      overflow: "auto",
    }

    if (!visible) style.display = "none";

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
          <img src={image} alt="" />
          <div className="post__footer">
            <Button
              onClick={showMe}
              type="submit"
              style={{alignItems: "normal"}}
            >
              <ChatBubbleOutlineIcon fontSize="small" />
            </Button>
            <br></br>
            {visible && <div>
            <Button
              onClick={hideMe}
              type="submit"
              >
              &times;
            </Button>
            <Comments />
            </div>}
            <RepeatIcon fontSize="small" />
            <FavoriteBorderIcon fontSize="small" />
            <PublishIcon fontSize="small" />
          </div>
        </div>
      </div>
    );
  }
);

export default Post;
