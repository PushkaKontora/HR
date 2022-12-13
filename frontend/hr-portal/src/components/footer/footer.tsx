import footerLogo from '../../assets/img/footer/logo-footer.svg';

import './footer.scss';
import ContactsIcons from '../contacts-icons/contacts-icons';

function Footer() {
  return (
    <div className="footer-wrapper">
      <div className="footer-content">
        <div className="footer-side">
          <img src={footerLogo} alt="logo-footer"/>
        </div>
        <ContactsIcons/>
      </div>
    </div>
  );
}

export default Footer;