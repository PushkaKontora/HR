import React from 'react';

import logoHeader from '../../assets/img/header/logo_m.svg';
import personalIcon from '../../assets/img/header/personal.svg';

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import {ReactComponent  as LikeIcon} from '../../assets/img/header/default-likes.svg';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import {ReactComponent  as PersonalIcon} from '../../assets/img/header/personal.svg';
import exitIcon from '../../assets/img/header/button-exit.svg';
import './header.scss';
import HeaderNav from '../header-nav/header-nav';

function Header() {

  return (
    <div className="header-wrapper">
      <div className="header-content">
        <div className="side-header side-header__leftSide">
          <div className="logo-header-wrapper">
            <img src={logoHeader} alt="logo"/>
          </div>
          <HeaderNav/>
        </div>
        <div className="side-header">
          <div className="header-nav-personal"><LikeIcon className='likes-icon'/></div>
          <div className="header-nav-personal"><PersonalIcon className='personal-icon' /></div>
          <div className="header-nav-personal"><img src={exitIcon} alt="exit icon"/></div>
        </div>
      </div>
    </div>
  );
}

export default Header;