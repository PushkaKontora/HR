import {Vacancy} from '../../types/vacancy';
import {ExpectedExperience} from '../../const';
import VacancyCard from '../../components/vacancy-card/vacancy-card';
import {Content} from '../../components/styled/markup/content';
import {ResumeUser} from '../../types/resume';
import {ExperienceOptions} from '../../types/experience-options';
import ResumeCard from '../../components/resume-card/resume-card';
import {FavoriteTabManager} from '../../components/favorite-tab-manager/favorite-tab-manager';
import {useEffect, useState} from 'react';
import {SubHeader} from './styled';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {getTabsByUserStatus} from '../../utils/favorite';
import {getVacancyWishlist, VacancyWishListSortBy} from '../../service/async-actions/async-actions-vacancy';
import {UserStatus} from '../../types/user-status';
import {getResumeWishlist, ResumeWishListSortBy} from '../../service/async-actions/async-actions-resume';
import VacancyList from '../../components/vacancy-list/vacancy-list';

export function FavoritePage() {
  const vacMock: Vacancy = {
    'id': 1,
    'name': 'Поооооовар',
    'description': 'Берем сначала ложку, потом коровию лепешку',
    'expected_experience': ExpectedExperience.FROM_ONE_TO_THREE_YEARS,
    'salary_from': 10000,
    'salary_to': 20000,
    'department': {
      'id': 1,
      'name': 'Департамент поваров',
      'description': 'Aaaaa!',
      'leader': {
        'id': 1,
        'surname': 'Jobs',
        'name': 'Povar',
        'patronymic': ''
      }
    },
    'published_at': new Date(Date.now())
  };
  const resumeMock: ResumeUser = {
    'id': 101,
    'owner': {
      'surname': 'Tsar',
      'name': 'Peter The Great',
      'patronymic': '',
      'email': 'email@employer.com',
      'photo': ''
    },
    'desired_job': 'Менеджер над менеждерами',
    'desired_salary': 100000,
    'experience': 'from_three_to_six_years',
    'document': '123456789_my-cool-resume.pdf',
    'published_at': new Date(Date.now()),
    'competencies': ['JS', 'TS', 'PS5']
  };

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
