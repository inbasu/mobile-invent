import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useContext, useEffect, useState } from 'react';
import { ActionContext, DataContext, ItemsContext, ItemContext, LoadingContext, ResultContext, StoresContext } from '../context';
import { Item } from '../datatypes';
import Grid from '@mui/material/Grid2';
import axios from "axios";
import { UserContext } from '../../App';


const search = (items: Array<Item>, action: string) => {
        switch (action) {
                case "takeback":
                        return items.filter((item) => {

                                return item.attrs.filter(attr => {

                                        return ((attr.name == "State" && attr.values[0].label == "Working") ||
                                                (attr.name == "User" && attr.values.length))
                                }).length

                        })
                case "giveaway":
                        return items.filter((item) => item.itreq)
                case "send":
                        return items.filter((item) => {
                                return item.attrs.filter((attr) => {
                                        return (attr.name == "State" && attr.values[0].label == "ApprovedToBeSent")
                                }).length
                        })
        }
        return items

}


export default function ActionSelect() {
        const user = useContext(UserContext);
        const [items, setItems] = useContext(ItemsContext);
        const [results, setResults] = useContext(ResultContext);
        const [action, setAction] = useContext(ActionContext);
        const [data, setData] = useContext(DataContext);
        const [item, setItem] = useContext(ItemContext);
        const [loading, setLoading] = useContext(LoadingContext);
        const [stores, setStores] = useContext(StoresContext);

        const [store, setStore] = useState<string | undefined>();
        useEffect(() => {
                const result = search(data, action)
                setItems(result);
                setResults(result);
        }, [action])


        useEffect(() => {
                setData([]);
                setItems([]);
                setResults([]);
                setItem(null);
                setLoading(true);
                axios.post(`http://127.0.0.1:8800/mobile/items/`,
                        { 'store': store })
                        .then((response) => {
                                setData(response.data);
                                const result = search(response.data, action)
                                setItems(result);
                                setResults(result);
                        }).finally(() => { setLoading(false) })
                        ;

        }, [store])

        return (
                <Grid container>
                        <Grid size={6} pr={1}>
                                <FormControl fullWidth>
                                        <InputLabel id="store-select-label">ТЦ</InputLabel>
                                        <Select
                                                labelId="store-select-label"
                                                id="action-select"
                                                value={store}
                                                label="ТЦ"
                                                disabled={loading}
                                                onChange={(event) => setStore(event.target.value)}>
                                                {user.roles.includes("MCC_RU_INSIGHT_IT_ROLE") && stores ?
                                                        stores.map(s => {
                                                                return (
                                                                        <MenuItem value={s.label}>{s.label}</MenuItem>
                                                                )
                                                        })
                                                        : user.store_role.map(s => {
                                                                return (
                                                                        <MenuItem value={s} selected>{s}</MenuItem>
                                                                )
                                                        })

                                                }

                                        </Select>
                                </FormControl >
                        </Grid>

                        <Grid size={6}>
                                <FormControl fullWidth>
                                        <InputLabel id="action-select-label">{store && 'Выберите действие'}</InputLabel>
                                        <Select
                                                labelId="action-select-label"
                                                id="action-select"
                                                value={action}
                                                label="Выберите действие"
                                                disabled={loading || !store}
                                                onChange={(event) => setAction(event.target.value)}>
                                                <MenuItem value={""}>Посмотреть</MenuItem>
                                                <MenuItem value={"giveaway"}>Выдать</MenuItem>
                                                <MenuItem value={'takeback'}>Сдать</MenuItem>
                                                <MenuItem value={'send'}>Переслать</MenuItem>
                                        </Select>
                                </FormControl >
                        </Grid>
                </Grid>
        )
}
