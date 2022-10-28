import footerLogo from '../../assets/img/footer/logo-footer.svg';
import iconCompany from '../../assets/img/footer/logo-company.svg';
import logoVK from '../../assets/img/footer/logo-vk.svg';
import logoWEB from '../../assets/img/footer/logo-web.svg';
import './footer.scss';

function Footer() {
  return (
    <div className="footer-wrapper">
      <div className="footer-content">
        <div className="footer-side">
          <img src={footerLogo} alt="logo-footer"/>
        </div>
        <div className="footer-side footer-side__contact">
          <div className="footer-nav"><img src={iconCompany} alt="icon Company"/></div>
          <div className="footer-nav"><img src={logoVK} alt="logo VK"/></div>
          <div className="footer-nav"><img src={logoWEB} alt="logo WEB"/></div>
        </div>
      </div>
    </div>
  );
}

export default Footer;