import {createSlice} from '@reduxjs/toolkit';
import {ButtonVacancyCard, TabInHeader} from '../../const';

interface PageSlice {
  buttonVacancyCard: ButtonVacancyCard;
  activeTabInHeader: TabInHeader | null;
}

const initialState: PageSlice = {
  buttonVacancyCard: ButtonVacancyCard.vacancies,
  activeTabInHeader: TabInHeader.vacancies
};

const pageSlice = createSlice({
  name: 'page',
  initialState,
  reducers: {
    changeButtonVacancyCard(state, action) {
      state.buttonVacancyCard = action.payload;
    },
    changeActiveTabInHeader(state, action) {
      state.activeTabInHeader = action.payload;
    }
  }
});

export const {
  changeButtonVacancyCard,
  changeActiveTabInHeader
} = pageSlice.actions;

export default pageSlice.reducer;