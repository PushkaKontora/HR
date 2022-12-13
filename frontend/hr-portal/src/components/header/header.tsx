import './header.scss';
import {useAppSelector} from '../../app/hooks';

import {UserStatus} from '../../types/user-status';
import HeaderAuth from '../header-auth/header-auth';
import HeaderNoAuth from '../header-noAuth/header-noAuth';

function Header() {
  const status = useAppSelector((state) => state.general.statusUser);

  return (
    <div className="header-wrapper">
      {status === UserStatus.noAuth
        ? (
          <HeaderNoAuth/>
        ) : (
          <HeaderAuth/>
        )
      }
    </div>
  );
}

export default Header;