// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import {ReactComponent as LogoVK} from '../../assets/img/footer/logo-vk.svg';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import {ReactComponent as LogoWeb} from '../../assets/img/footer/logo-web.svg';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import {ReactComponent as LogoCompany} from '../../assets/img/footer/logo-company.svg';

import './contacts-icons.scss';

function ContactsIcons() {
  return (
    <div className="contact">
      <a href="https://www.interesnee.ru/" className="footer-nav">
        <LogoCompany className="logoCompany"/>
      </a>
      <a href="https://vk.com/interesnee_ru" className="footer-nav">
        <LogoVK className="logoVK"/>
      </a>
      <a href="https://www.linkedin.com/company/interesnee-ru/" className="footer-nav">
        <LogoWeb className="logoLinkin"/>
      </a>
    </div>
  );
}

export default ContactsIcons;