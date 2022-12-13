import './tab-state-my-vacancy.scss';
import {BlueButton} from '../styled/buttons/blue-button';
import {GrayButton} from '../styled/buttons/gray-button';
import {setIsPublishedVacancy} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch, useAppSelector} from '../../app/hooks';

function TabStateMyVacancy() {
  const stateMyVacancyPublish = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const dispatch = useAppDispatch();

  return (
    <div className="tab-state-my-vacancy">
      {stateMyVacancyPublish
        ? (
          <>
            <BlueButton as="button" padding="24px 40px">Опубликованные вакансии</BlueButton>
            <GrayButton
              as="button"
              padding="24px 40px"
              onClick={() => dispatch(setIsPublishedVacancy(false))}
            >Неопубликованные вакансии
            </GrayButton>
          </>
        ) : (
          <>
            <GrayButton as="button" padding="24px 40px" onClick={() => dispatch(setIsPublishedVacancy(true))}>Опубликованные вакансии</GrayButton>
            <BlueButton as="button" padding="24px 40px">Неопубликованные вакансии</BlueButton>
          </>
        )
      }
    </div>
  );
}

export default TabStateMyVacancy;