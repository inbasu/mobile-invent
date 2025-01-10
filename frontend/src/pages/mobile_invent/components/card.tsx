import Grid from "@mui/material/Grid2";
import { Values } from "../datatypes"
import ButtonGroup from "./buttonsGrp";
import { useContext } from "react";
import { ActionContext, ItemContext, StoreContext } from "../context";
import { Typography } from "@mui/material";

import Button from '@mui/material/Button';
import { Box, IconButton } from "@mui/material";

const hardwareFields = ["INV No", "Store", "Serial No", "Model", "State", "Location", "User", "Store"];
const ereqFields = ["Store", "Кто выдал", 'Дата выдачи', "Пользователь", 'Кто принял', 'Дата сдачи'];
const jiraFields = ['Key', 'Issue Location', 'For user', 'inv.'];


const AttrRow = ({ attr }: { attr: Values }) => {
        return (
                <>
                        <Grid size={4}>{attr.name}:</Grid>
                        <Grid size={8}>{attr.values[0] ? attr.values[0].label : ''}</Grid>
                </>)
}



export default function ItemCard() {
        const [item, _setItem] = useContext(ItemContext);
        const [action, _setAction] = useContext(ActionContext);
        const [store, _setStore] = useContext(StoreContext);

        return (
                <Grid container p={2}>
                        {item?.id === 0 ? <Grid size={12}><h3>{item?.label}</h3></Grid> : <Grid size={12}><h3>{item?.itreq?.Key}</h3></Grid>}
                        <Grid size={12}><Typography variant='overline'>Оборудование</Typography></Grid>
                        {item?.id !== 0 ?
                                <Grid container size={12} pb={3}>
                                        {item?.attrs && item.attrs.map(attr => {
                                                if (hardwareFields.includes(attr.name) && attr.values) {
                                                        return (<AttrRow attr={attr} />)
                                                }
                                        })}
                                </Grid>
                                :
                                <Grid p={1}>
                                        <Box sx={{ border: "solid red 1px" }}>
                                                <Typography variant="button" color={"error"}>
                                                        К сожаленю произошла ошибка, <br />
                                                        К запросу на выдачу некорректно проставленно оборудование.<br />
                                                        Пожалуйста обратиесть в поддержку.:wq
                                                </Typography>
                                        </Box>
                                </Grid>
                        }
                        {item?.joined.length !== 0 ?
                                <Grid container size={12} pb={3}>
                                        <Grid size={12}><Typography variant='overline'>Карточка</Typography></Grid>
                                        {item?.joined && item.joined[0]?.attrs?.map(attr => {
                                                if (ereqFields.includes(attr.name)) {
                                                        return (<AttrRow attr={attr} />)
                                                }
                                        })
                                        }
                                </Grid> :
                                <Grid p={1} size={12}>
                                        <Box sx={{
                                                border: "solid red 1px",
                                                borderRadius: "6px",
                                                padding: "3px", display: "flex",
                                                justifyContent: "center",
                                                alignItems: "center",
                                                flexDirection: "column",
                                                width: "100%"
                                        }}>

                                                <Typography variant="button" color={"error"}>
                                                        К сожаленю произошла ошибка,<br />
                                                        Данное оборудование невозможно сдать через asset-tool<br />
                                                        Оно было выданно без соответствующей карточки<br />
                                                </Typography>
                                                <Button>Сообщить о проблеме</Button>
                                        </Box>
                                </Grid>

                        }
                        {
                                item?.itreq &&
                                <Grid container size={12} pb={3}>
                                        <Grid size={12}><Typography variant='overline'>Заявка</Typography></Grid>
                                        {item?.itreq && jiraFields.map(attr => {
                                                return (
                                                        <>
                                                                <Grid size={4}>{attr}</Grid>
                                                                <Grid size={8}>{item?.itreq[attr] ? item?.itreq[attr] : ""}</Grid>
                                                        </>)
                                        })}
                                </Grid>
                        }
                        <Grid size={12}>
                                {action && item?.id !== 0 ? <ButtonGroup /> : ''}
                        </Grid>
                </Grid >)
}
