import iconCompany from '../../assets/img/footer/logo-company.svg';
import logoVK from '../../assets/img/footer/logo-vk.svg';
import logoWEB from '../../assets/img/footer/logo-web.svg';
import './contacts-icons.scss';

function ContactsIcons() {
  return (
    <div className="contact">
      <div className="footer-nav"><img src={iconCompany} alt="icon Company"/></div>
      <div className="footer-nav"><img src={logoVK} alt="logo VK"/></div>
      <div className="footer-nav"><img src={logoWEB} alt="logo WEB"/></div>
    </div>
  );
}

export default ContactsIcons;