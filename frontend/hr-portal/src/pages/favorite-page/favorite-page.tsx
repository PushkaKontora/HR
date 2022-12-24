import {Content} from '../../components/styled/markup/content';

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
import ModalRespondRequest from '../../components/modal-respond-request/modal-respond-request';
import {changeActiveTabInHeader, changeButtonVacancyCard} from '../../features/page/page-slice';
import {ButtonVacancyCard} from '../../const';

export function FavoritePage() {
  const dispatch = useAppDispatch();
  const user = useAppSelector((state) => state.general.user);
  const favoriteVacancies = useAppSelector((state) => state.user.favoriteVacancies);
  const favoriteResume = useAppSelector((state) => state.user.favoriteResumes);

  const [vacancyLength, setVacancyLength] = useState(favoriteVacancies.length);
  const [resumeLength, setResumeLength] = useState(favoriteResume.length);
  const [currentTabIndex, setCurrentTabIndex] = useState(0);

  useEffect(() => {
    dispatch(changeActiveTabInHeader(null));
    dispatch(changeButtonVacancyCard(ButtonVacancyCard.favorite));
  }, []);

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      dispatch(getVacancyWishlist(VacancyWishListSortBy.added_at_desc));
      //.then(() => setVacancyLength(favoriteVacancies.length));

      if (user?.permission === UserStatus.employer) {
        dispatch(getResumeWishlist(ResumeWishListSortBy.added_at_desc));
        //.then(() => setResumeLength(favoriteResume.length));
      }
    }

    return () => {
      mounted = false;
    };
  }, [user]);

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      if (favoriteVacancies)
        setVacancyLength(favoriteVacancies.length);

      if (favoriteResume)
        setResumeLength(favoriteResume.length);
    }

    return () => {
      mounted = false;
    };
  }, [favoriteResume, favoriteVacancies]);

  const onTabChange = (index: number) => {
    setCurrentTabIndex(index);
  };

  return (
    <div>
      <ModalRespondRequest/>
      <Content>
        <img src={banner} style={{marginBottom: '24px'}}/>
        <HorizontalLine/>
        <SubHeader>
          {
            user?.permission === UserStatus.employer &&
            <>
              <FavoriteTabManager
                tabNames={getTabsByUserStatus(user?.permission)}
                clickHandler={onTabChange}/>
              <div style={{flexGrow: 2}}/>
            </>
          }
          <h3 style={{whiteSpace: 'nowrap'}}>
            Добавлено&nbsp;
            {currentTabIndex == 0 && `${vacancyLength} вакансий`}
            {currentTabIndex == 1 && `${resumeLength} резюме`}
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
