import logoHeader from '../../assets/img/header/logo_m.svg';
import likeIcon from '../../assets/img/header/likes.svg';
import personalIcon from '../../assets/img/header/personal.svg';
import exitIcon from '../../assets/img/header/button-exit.svg';
import {useAppSelector} from '../../app/hooks';
import {UserStatus} from '../../types/user-status';
import {Fragment} from 'react';

function Header() {
  const statusUser = useAppSelector((state) => state.general.statusUser);

  return (
    <div className="header-wrapper">
      <div className="side-header">
        <div className="logo-header-wrapper"><img src={logoHeader} alt="logo"/></div>
        <div className="header-nav">
          <div className="header-navItem">Вакансии</div>
          {statusUser !== UserStatus.user ? (
            <Fragment>
              <div className="header-navItem">Резюме</div>
              <div className="header-navItem">Мои вакансии</div>
            </Fragment>
          ) : undefined}
        </div>
      </div>
      <div className="side-header">
        <div className="header-nav-personal"><img src={likeIcon} alt="like icon"/></div>
        <div className="header-nav-personal"><img src={personalIcon} alt="personal icon"/></div>
        <div className="header-nav-personal"><img src={exitIcon} alt="exit icon"/></div>
      </div>
    </div>
  );
}

export default Header;