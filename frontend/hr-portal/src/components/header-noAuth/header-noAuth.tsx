import './header-noAuth.scss';
import logoHeader from '../../assets/img/header/logo_m.svg';
import ContactsIcons from '../contacts-icons/contacts-icons';

function HeaderNoAuth() {
  return (
    <div className="header-no-auth-wrapper">
      <div className="logo-header-wrapper">
        <img src={logoHeader} alt="logo"/>
      </div>
      <ContactsIcons/>
    </div>
  );
}

export default HeaderNoAuth;