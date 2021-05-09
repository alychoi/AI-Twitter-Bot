import React, { useState, useEffect } from 'react';
import Feed from "./Feed";
import Widgets from "./Widgets";
import "./App.css";
import { BrowserRouter, Link, Route, Switch } from 'react-router-dom';
import "./Sidebar.css";
import TwitterIcon from "@material-ui/icons/Twitter";
import SidebarOption from "./SidebarOption";
import HomeIcon from "@material-ui/icons/Home";
import SearchIcon from "@material-ui/icons/Search";
import NotificationsNoneIcon from "@material-ui/icons/NotificationsNone";
import MailOutlineIcon from "@material-ui/icons/MailOutline";
import BookmarkBorderIcon from "@material-ui/icons/BookmarkBorder";
import ListAltIcon from "@material-ui/icons/ListAlt";
import PermIdentityIcon from "@material-ui/icons/PermIdentity";
import MoreHorizIcon from "@material-ui/icons/MoreHoriz";
import { Button } from "@material-ui/core";

function App() {

  return (
    // BEM
    <div className="app">
    <BrowserRouter>
    <div className="sidebar">
      <Link to="/home"><TwitterIcon className="sidebar__twitterIcon" /></Link>
      <Link to="/home"><SidebarOption active Icon={HomeIcon} text="Home" /></Link>
      <Link to="/explore"><SidebarOption Icon={SearchIcon} text="Explore" /></Link>
      <Link to="/notifications"><SidebarOption Icon={NotificationsNoneIcon} text="Notifications" /></Link>
      <Link to="/messages"><SidebarOption Icon={MailOutlineIcon} text="Messages" /></Link>
      <Link to="/bookmarks"><SidebarOption Icon={BookmarkBorderIcon} text="Bookmarks" /></Link>
      <Link to="/lists"><SidebarOption Icon={ListAltIcon} text="Lists" /></Link>
      <Link to="/profile"><SidebarOption Icon={PermIdentityIcon} text="Profile" /></Link>
      <Link to="/more"><SidebarOption Icon={MoreHorizIcon} text="More" /></Link>
      

      {/* Button -> Tweet */}
      <Button variant="outlined" className="sidebar__tweet" fullWidth>
        Tweet 
      </Button>
    </div>
        <Switch>
            <Route path="/home">
              <Feed />
              <Widgets />
            </Route>
        </Switch>
        </BrowserRouter>
    </div>
  );
}

export default App;
