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
      <a href="https://www.interesnee.ru/" target='_blank' className="footer-nav" rel="noreferrer">
        <LogoCompany className="logoCompany"/>
      </a>
      <a href="https://vk.com/interesnee_ru" target='_blank' className="footer-nav" rel="noreferrer">
        <LogoVK className="logoVK"/>
      </a>
      <a href="https://www.linkedin.com/company/interesnee-ru/" target='_blank' className="footer-nav" rel="noreferrer">
        <LogoWeb className="logoLinkin"/>
      </a>
    </div>
  );
}

export default ContactsIcons;