import { useContext, useEffect, useState } from "react";
import Grid from "@mui/material/Grid2";
import axios from "axios";

import Button from '@mui/material/Button';
import { ActionContext, ItemContext, StoreContext, StoresContext } from "../context";
import { styled } from "@mui/material/styles";
import { Autocomplete, TextField, Typography } from "@mui/material";
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import SendIcon from '@mui/icons-material/Send';
import { Item } from "../datatypes";
import { API_URL } from "../page";


const actionMap = new Map([['takeback', "Сдать"], ["giveaway", "Выдать"], ["send", "Переслать"]])
const blankMaxSize = 1024;
const blankFormats = [".pdf", ".jpg", ".jpeg", ".png"]

const HiddenInput = styled('input')({
        clip: 'rect(0 0 0 0)',
        clipPath: 'insert(50%)',
        height: 1,
        overflow: 'hidden',
        position: 'absolute',
})


const AutocompleteField = (data: Array<Item> | null, selected: Item | null, setData: Function, label: string) => {
        return (
                <Autocomplete
                        options={data ? data : []}
                        getOptionLabel={(option) => option.label}
                        value={selected}
                        onChange={(_, value) => setData(value)}
                        renderInput={(params) => <TextField {...params} label={label} size="small" fullWidth />}
                />
        )
}



export default function ButtonGroup() {
        const [action, _setAction] = useContext(ActionContext);
        const [item, _setItem] = useContext(ItemContext);
        const [stores, _setStores] = useContext(StoresContext);
        const [store, _setStore] = useContext(StoreContext);
        const [blank, setBlank] = useState<File | null>(null);
        const [validBlank, setValidBlank] = useState<boolean | null>(null)

        const [to_store, setToStore] = useState<Item | null>(null);
        const [trackCode, setTrackCode] = useState<string | null>(null);

        const handleDownload = () => {
                axios.post(`${API_URL}/blank/`, { action: action, item: item }, { responseType: "blob" })
                        .then(response => {
                                const type = response.headers["content-type"];
                                const url = window.URL.createObjectURL(new Blob([response.data], { type: type }));
                                const link = document.createElement("a");
                                link.href = url;
                                link.setAttribute("download", `${item?.label}.docx`);
                                document.body.appendChild(link);
                                link.click();
                                link.parentNode?.removeChild(link);
                        })
        };

        const handleUpload = (file: File | null) => {
                if (file && blankMaxSize > (file?.size / 1024) && blankFormats.some(suff => file.name.endsWith(suff))) {
                        setBlank(file);
                        setValidBlank(true);
                        console.log(123)
                } else {
                        setBlank(null);
                        setValidBlank(false);
                }
        };

        const handleAction = () => {
                if (!validBlank) {
                        return
                }
                const formData = new FormData();
                formData.append('action', action);
                formData.append('item', JSON.stringify(item));
                formData.append('blank', blank ? blank : '');
                formData.append('store', JSON.stringify(store));
                formData.append('track', JSON.stringify(trackCode));
                formData.append('to_store', JSON.stringify(to_store));

                console.log(...formData.entries())
                axios.post(`${API_URL}/action/`, formData)
                        .then((response) => {
                                if (response.data.error) {
                                        console.log(123)
                                } else {
                                        console.log(321)
                                }

                        })
        }


        useEffect(() => {
                setBlank(null);
                setValidBlank(false);
                console.log(action)
        }, [item, action])

        return (
                <Grid container spacing={1}>
                        <Grid size={3}>
                                {action !== "send" ?
                                        <Button variant="text"
                                                color={"secondary"}
                                                onClick={handleDownload}
                                        >Скачать бланк
                                                <FileDownloadIcon />
                                        </Button>
                                        :
                                        AutocompleteField(
                                                stores,
                                                to_store,
                                                setToStore,
                                                "ТЦ"
                                        )
                                }
                        </Grid>
                        <Grid size={6}>
                                {action !== "send" ?
                                        <>
                                                <Button variant="outlined"
                                                        color={validBlank ? "success" : 'error'}
                                                        component="label"
                                                        fullWidth>
                                                        {blank ? blank.name : "Выберите файл"}
                                                        <HiddenInput type="file" onChange={(event) => handleUpload(event.target.files ? event.target.files[0] : null)} />
                                                </Button>
                                                {!validBlank && (
                                                        <Typography textAlign={"center"} color={"error"}>
                                                                Файл в формате <b>.pdf</b> и рамером менее 0.5мб
                                                        </Typography>)}
                                        </>
                                        : <TextField size="small"
                                                label="Трек код"
                                                onChange={(event) => setTrackCode(event.target.value)}
                                                fullWidth />
                                }
                        </Grid>



                        <Grid size={2.5}>
                                {action &&
                                        <Button variant="contained"
                                                onClick={handleAction}
                                                fullWidth
                                                disabled={!validBlank}
                                        >{actionMap.get(action)}
                                                <SendIcon />
                                        </Button>
                                }
                        </Grid>
                </Grid>
        )
}
