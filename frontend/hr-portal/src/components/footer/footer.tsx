import footerLogo from '../../assets/img/footer/logo-footer.svg';

import './footer.scss';
import ContactsIcons from '../contacts-icons/contacts-icons';
import {Link} from 'react-router-dom';

function Footer() {
  return (
    <div className="footer-wrapper">
      <div className="footer-content">
        <Link to={'/'} className="footer-side">
          <img src={footerLogo} alt="logo-footer"/>
        </Link>
        <ContactsIcons/>
      </div>
    </div>
  );
}

export default Footer;