import {Link} from 'react-router-dom';

import {UserStatus} from '../../types/user-status';
import cl from 'classnames';
import {useAppSelector} from '../../app/hooks';
import {TabInHeader} from '../../const';

function HeaderNav() {
  const statusUser = useAppSelector((state) => state.general.statusUser);
  const activeTab = useAppSelector((state) => state.page.activeTabInHeader);

  return (
    <>
      {statusUser !== UserStatus.noAuth && (
        <div className="header-nav">
          {statusUser === UserStatus.user
          && (<Link to="/" className={cl('header-navItem', {'header-navItem__active': activeTab === TabInHeader.vacancies})}>
            Вакансии
          </Link>)
          }
          {statusUser === (UserStatus.employer || UserStatus.admin) && (
            <>
              <div className={cl('header-navItem', {'header-navItem__active': activeTab === TabInHeader.vacancies})}>
                Вакансии
              </div>
              <div className={cl('header-navItem', {'header-navItem__active': activeTab === TabInHeader.resume})}>
                Резюме
              </div>
              <Link to="/" className={cl('header-navItem', {'header-navItem__active': activeTab === TabInHeader.myVacancy})}>
                Мои вакансии
              </Link>
            </>
          )}
        </div>
      )}
    </>
  );
}

export default HeaderNav;