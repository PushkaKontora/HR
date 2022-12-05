import {Vacancy} from '../../types/vacancy';
import {ExpectedExperience} from '../../const';
import VacancyCard from '../../components/vacancy-card/vacancy-card';
import {Content} from '../../components/styled/markup/content';
import {ResumeUser} from '../../types/resume';
import {ExperienceOptions} from '../../types/experience-options';
import ResumeCard from '../../components/resume-card/resume-card';
import {FavoriteTabManager} from '../../components/favorite-tab-manager/favorite-tab-manager';
import {useEffect, useState} from 'react';
import {SubHeader, HorizontalLine} from './styled';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {getTabsByUserStatus} from '../../utils/favorite';
import {getVacancyWishlist, VacancyWishListSortBy} from '../../service/async-actions/async-actions-vacancy';
import {UserStatus} from '../../types/user-status';
import {getResumeWishlist, ResumeWishListSortBy} from '../../service/async-actions/async-actions-resume';
import VacancyList from '../../components/vacancy-list/vacancy-list';
import banner from '../../assets/img/favorites/banner.svg';

export function FavoritePage() {
  const dispatch = useAppDispatch();
  const user = useAppSelector((state) => state.general.user);
  const favoriteVacancies = useAppSelector((state) => state.user.favoriteVacancies);
  const favoriteResume = useAppSelector((state) => state.user.favoriteResumes);

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      dispatch(getVacancyWishlist(VacancyWishListSortBy.added_at_desc));

      if (user?.permission === UserStatus.employer) {
        dispatch(getResumeWishlist(ResumeWishListSortBy.added_at_desc));
      }
    }

    return () => {
      mounted = false;
    };
  }, [user]);

  const [currentTabIndex, setCurrentTabIndex] = useState(0);
  const onTabChange = (index: number) => {
    setCurrentTabIndex(index);
  };

  return (
    <div>
      <Content>
        <img src={banner} style={{marginBottom: '24px'}}/>
        <HorizontalLine/>
        <SubHeader>
          <FavoriteTabManager
            tabNames={getTabsByUserStatus(user?.permission)}
            clickHandler={onTabChange}/>
          <h3 style={{flex: 1, textAlign: 'right'}}>
            Добавлено&nbsp;
            {currentTabIndex == 0 && `${favoriteVacancies?.length || 0} вакансий`}
            {currentTabIndex == 1 && `${favoriteResume?.length || 0} резюме`}
          </h3>
        </SubHeader>
        {
          currentTabIndex == 0 && 
            <section style={{marginBottom: '128px'}}>
              <VacancyList vacancies={favoriteVacancies} showPagination={false}/>
            </section>
        }
        {
          currentTabIndex == 1 &&
          <section style={{marginBottom: '128px'}}>
            {
              favoriteResume.map((item, idx) => {
                return (
                  <ResumeCard key={idx} resume={item}/>
                );
              })
            }
          </section>
        }
      </Content>
    </div>
  );
}
