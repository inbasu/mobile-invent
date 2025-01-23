import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useContext, useEffect } from 'react';
import { ActionContext, DataContext, ItemsContext, ItemContext, LoadingContext, ResultContext, StoresContext, StoreContext, QuerryContext } from '../context';
import { actionFilter, querryFilter } from '../search';
import Grid from '@mui/material/Grid2';
import axios from "axios";
import { UserContext } from '../../../App';




export default function ActionSelect() {
        const user = useContext(UserContext);
        const [_items, setItems] = useContext(ItemsContext);
        const [_results, setResults] = useContext(ResultContext);
        const [action, setAction] = useContext(ActionContext);
        const [querry, setQuerry] = useContext(QuerryContext);

        const [data, setData] = useContext(DataContext);
        const [_item, setItem] = useContext(ItemContext);
        const [loading, setLoading] = useContext(LoadingContext);
        const [stores, _setStores] = useContext(StoresContext);
        const [store, setStore] = useContext(StoreContext);


        useEffect(() => {
                setData([]);
                setItems([]);
                setResults([]);
                setQuerry('')
                setItem(null);
                if (store !== null && store !== "IT") {
                        setLoading(true);
                        axios.post(`http://127.0.0.1:8800/mobile/items/`,
                                { 'store': store })
                                .then((response) => {
                                        setData(response.data);
                                        const result = actionFilter(response.data, action, store);
                                        setItems(result);
                                        setResults(result);

                                }).finally(() => { setLoading(false) })
                                ;
                }

        }, [store])


        useEffect(() => {
                const actionItems = actionFilter(data, action, store);
                setItems(actionItems);
                const resultItems = querryFilter(actionItems, querry);
                setResults(resultItems);
                setItem(null);
        }, [action])
        //AND "УНАДРТЦ" IS NOT EMPTY AND "Jira issue location" IS NOT EMPTY
        return (
                <Grid container>
                        <Grid size={6} pr={1}>
                                <FormControl fullWidth>
                                        <InputLabel id="store-select-label">1.ТЦ</InputLabel>
                                        <Select
                                                labelId="store-select-label"
                                                id="action-select"
                                                value={store}
                                                label="1.ТЦ"
                                                disabled={loading}
                                                onChange={(event) => setStore(event.target.value)}>
                                                {user.roles.includes("MCC_RU_INSIGHT_IT_ROLE") ? <MenuItem value="IT">IT</MenuItem> : ''}
                                                {user.roles.includes("MCC_RU_INSIGHT_IT_ROLE") ?
                                                        stores && stores.map(s => {
                                                                if (s.attrs.filter(attr => (attr.name === "Jira issue location" || attr.name == "УНАДРТЦ")).length == 2) {
                                                                        return (
                                                                                <MenuItem value={JSON.stringify(s)}>{s.label}</MenuItem>
                                                                        )
                                                                }
                                                        })
                                                        : stores && stores.filter(s => user.store_role.includes(s.label)).map(s => {
                                                                return (
                                                                        <MenuItem value={JSON.stringify(s)}>{s.label}</MenuItem>
                                                                )
                                                        })

                                                }

                                        </Select>
                                </FormControl >
                        </Grid>

                        <Grid size={6}>
                                <FormControl fullWidth>
                                        <InputLabel id="action-select-label">{store && '2.Выберите действие'}</InputLabel>
                                        <Select
                                                labelId="action-select-label"
                                                id="action-select"
                                                value={action}
                                                label="2.Выберите действие"
                                                disabled={loading || !store}
                                                onChange={(event) => setAction(event.target.value)}>
                                                {store !== "IT" && <MenuItem value={""}>Посмотреть</MenuItem>}
                                                <MenuItem value={"giveaway"}>Выдать</MenuItem>
                                                <MenuItem value={'takeback'}>Сдать</MenuItem>
                                                <MenuItem value={'send'}>Переслать</MenuItem>
                                        </Select>
                                </FormControl >
                        </Grid>
                </Grid>
        )
}
