import Modal from '../../reused-components/modal/modal';
import React, {ChangeEvent, useEffect, useState} from 'react';
import {DepartmentsShortVersions, setIsEditorVacancyFlag, setIsOpenEditVacancyModal, setIsStartRequestChangeVacancy, setSalaryMax, setSalaryMin, setStateEditVacancy} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import './modal-edit-vacancy.scss';
import '../../styles/btn-blue-disabled.scss';
import cl from 'classnames';
import Select, {SingleValue} from 'react-select';
import {ExpectedExperience, ExpectedExperienceNameString, expectedExperienceShortVersion, TypeRequestVacancyModal} from '../../const';
import EmployerCreatingNewVacancy from '../employer-creating-new-vacancy/employer-creating-new-vacancy';
import {BlueButton} from '../styled/buttons/blue-button';
import {GrayButton} from '../styled/buttons/gray-button';
import {VacancyPutChangeParams} from '../../types/vacancy-put-change-params';
import {getVacanciesForEmployer, putVacancyChanges} from '../../service/async-actions/async-actions-vacancy';
import ModalBtnStatusVacancy from '../modal-btn-status-vacancy/modal-btn-status-vacancy';
import {refreshPageDetailsScreen} from '../../features/page/page-slice';

function ModalEditVacancy() {
  const typeRequestModalVacancy = useAppSelector((state) => state.vacancy.typeRequestModalVacancy);
  const vacancyByID = useAppSelector((state) => state.vacancy.vacancyByID);
  const isPublishedVacancy = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const isOpenEditVacancyModalState = useAppSelector((state) => state.vacancy.isOpenEditVacancyModal);
  const editorVacancyText = useAppSelector((state) => state.vacancy.editorTextVacancy);
  const isStartRequestChangeVacancy = useAppSelector((state) => state.vacancy.isStartRequestChangeVacancy);
  const [isOpenEditVacancy, setIsOpenEditVacancy] = useState(isOpenEditVacancyModalState);
  const [isPublishStatus, setIsPublishStatus] = useState(isPublishedVacancy);
  const [nameVacancy, setNameVacancy] = useState('');
  const [experience, setExperience] = useState<ExpectedExperience>(ExpectedExperience.NO_EXPERIENCE);
  const [minSalary, setMinSalary] = useState<number | null>(null);
  const [maxSalary, setMaxSalary] = useState<number | null>(null);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (isStartRequestChangeVacancy === true && typeRequestModalVacancy === TypeRequestVacancyModal.CHANGE) {
      const vacancyBody: VacancyPutChangeParams = {
        name: nameVacancy,
        description: editorVacancyText,
        expected_experience: experience,
        salary_from: minSalary,
        salary_to: maxSalary,
        published: isPublishStatus
      };
      if (vacancyByID) {
        dispatch(putVacancyChanges({idVacancy: vacancyByID.id, data: vacancyBody}))
          .then(() => {
            dispatch(getVacanciesForEmployer({isPublished: isPublishedVacancy, idDepartment: vacancyByID.department.id, offset: 0}))
              .then(() => {
                dispatch(refreshPageDetailsScreen(true));
                setIsOpenEditVacancy(false);
              });
          });
      }
      dispatch(setIsStartRequestChangeVacancy(false));
    }
  }, [isStartRequestChangeVacancy, editorVacancyText]);


  useEffect(() => {
    if (vacancyByID) {
      setNameVacancy(vacancyByID.name);
      if (vacancyByID?.salary_to) {
        setMaxSalary(vacancyByID?.salary_to);
      } else {
        setMaxSalary(null);
      }
      if (vacancyByID?.salary_from) {
        setMinSalary(vacancyByID?.salary_from);
      } else {
        setMinSalary(null);
      }
      if (vacancyByID?.expected_experience) {
        //setExperience(ExpectedExperience[vacancyByID?.expected_experience as ExpectedExperienceNameString]);
      }
    }
  }, [vacancyByID, isOpenEditVacancyModalState]);


  useEffect(() => {
    setIsOpenEditVacancy(isOpenEditVacancyModalState);
  }, [isOpenEditVacancyModalState]);

  useEffect(() => {
    dispatch(setIsOpenEditVacancyModal(isOpenEditVacancy));
  }, [isOpenEditVacancy]);

  const handleChangeNameVacancy = (e: ChangeEvent<HTMLInputElement>) => {
    setNameVacancy(e.target.value);
  };

  const onHandlerChangeExpectedExperience = (e: SingleValue<DepartmentsShortVersions>) => {
    if (e?.label) {
      const valueExp = Object.keys(ExpectedExperienceNameString).find(key => ExpectedExperienceNameString[key] === e.label);
      if (valueExp) {
        setExperience(valueExp as ExpectedExperience);
      }
    }
  };

  const handleChangeMinSalary = (e: ChangeEvent<HTMLInputElement>) => {
    const minValue = e.target.value;
    if (minValue) {
      setMinSalary(Number(minValue));
    } else {
      setMinSalary(null);
    }
  };

  const handleChangeMaxSalary = (e: ChangeEvent<HTMLInputElement>) => {
    const maxValue = e.target.value;
    if (maxValue) {
      setMaxSalary(Number(maxValue));
    } else {
      setMaxSalary(null);
    }
  };

  const putNewDescriptionVacancy = () => {
    if (nameVacancy.length > 0 && !(maxSalary !== null && minSalary !== null && maxSalary <= minSalary)) {
      dispatch(setIsEditorVacancyFlag(true));
    }
  };

  const handleUndoAction = (e: any) => {
    e.preventDefault();
    setIsOpenEditVacancy(false);
  };

  return (
    <Modal
      padding="80px 80px 60px 80px"
      width={1026}
      active={isOpenEditVacancy}
      setActive={setIsOpenEditVacancy}
    >
      <div className="edit-modal-item edit-modal-item__header">
        <div className="header header__title">Редактирование вакансии</div>
        <div className="header header__explanation">Заполните обязательные поля для редактирования вакансии</div>
      </div>
      <div className="edit-modal-item edit-modal-item__content">
        <div className="content-item">
          <div className="name-field">
            Статус вакансии*
          </div>
          <ModalBtnStatusVacancy isPublishStatus={isPublishStatus} setIsPublishStatus={setIsPublishStatus}/>
        </div>
        <div className="content-item">
          <div className="name-field">
            Название вакансии*
          </div>
          <input
            type="text"
            onChange={handleChangeNameVacancy}
            className="input-name-vacancy"
            value={nameVacancy}
          />
        </div>
        <div className="content-item">
          <div className="name-field">
            Опыт работы*
          </div>
          <Select
            className="basic-single"
            classNamePrefix="select"
            name=""
            options={expectedExperienceShortVersion}
            onChange={onHandlerChangeExpectedExperience}
            placeholder={ExpectedExperienceNameString[vacancyByID?.expected_experience as ExpectedExperience]}
          />
        </div>
        <div className="content-item">
          <div className="name-field">
            Зарплата
          </div>
          <div className="salaryInput-wrapper">
            <div className="text-field-salary text-field-salary__min">
              <input
                className="text-field-salary-input"
                type="number"
                min="0"
                onChange={handleChangeMinSalary}
                placeholder="min"
              />
            </div>
            <div className="text-field-salary text-field-salary__max">
              <input
                className="text-field-salary-input"
                type="number"
                min="0"
                onChange={handleChangeMaxSalary}
                placeholder="max"
              />
            </div>
          </div>
        </div>
        <div className="content-item content-item__description">
          <div className="name-field">
            Описание вакансии*
          </div>
          <EmployerCreatingNewVacancy typeViewToolbar={TypeRequestVacancyModal.CHANGE}/>
        </div>
      </div>
      <div className="edit-modal-item edit-modal-item__nav">
        <GrayButton as="button" onClick={handleUndoAction}>Отмена</GrayButton>
        <BlueButton as="button" className={cl({'disabledBlueBtn': nameVacancy.length <= 0 || (maxSalary !== null && minSalary !== null && maxSalary <= minSalary)})} onClick={putNewDescriptionVacancy}>
          Сохранить изменения
        </BlueButton>
      </div>
    </Modal>
  );
}

export default ModalEditVacancy;