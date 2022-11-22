import {UserStatus} from '../../types/user-status';
import cl from 'classnames';
import {useAppSelector} from '../../app/hooks';
import {TabInHeader} from '../../const';

function HeaderNav() {
  const statusUser = useAppSelector((state) => state.general.statusUser);
  const activeTab = useAppSelector((state) => state.user.activeTabInHeader);

  return (
    <>
      {statusUser !== UserStatus.noAuth && (
        <div className="header-nav">
          <div className={cl('header-navItem', {'header-navItem__active': activeTab === TabInHeader.vacancies})}>
            Вакансии
          </div>
          {statusUser === (UserStatus.employer || UserStatus.admin) && (
            <>
              <div className={cl('header-navItem', {'header-navItem__active': activeTab === TabInHeader.resume})}>
                Резюме
              </div>
              <div className={cl('header-navItem', {'header-navItem__active': activeTab === TabInHeader.myVacancy})}>
                Мои вакансии
              </div>
            </>
          )}
        </div>
      )}
    </>
  );
}

export default HeaderNav;