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
            <BlueButton as="button" width="293px" padding="24px 40px">Активные вакансии</BlueButton>
            <GrayButton
              as="button"
              width="293px"
              padding="24px 40px"
              onClick={() => dispatch(setIsPublishedVacancy(false))}
            >Нективные вакансии
            </GrayButton>
          </>
        ) : (
          <>
            <GrayButton as="button" width="293px" padding="24px 40px" onClick={() => dispatch(setIsPublishedVacancy(true))}>Активные вакансии</GrayButton>
            <BlueButton as="button" width="293px" padding="24px 40px">Нективные вакансии</BlueButton>
          </>
        )
      }
    </div>
  );
}

export default TabStateMyVacancy;