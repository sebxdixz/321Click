//page to show trabajos with mui/material/Card from api with axios
"use client";
import React, { Component } from 'react';
import { useRouter } from 'next/router'
import axios from 'axios';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

import { getServerSession } from 'next-auth/next'


export default class Trabajo extends Component {
    constructor(props) {
        super(props);
        this.state = {
        trabajos: []
        };
    }
    
    componentDidMount() {
        axios.get('http://localhost:4000/trabajo')
        .then(res => {
            this.setState({ trabajos: res.data });
        })
        .catch(function (error) {
            console.log(error);
        })
    }
    
    render() {
        return (
            <div className="h-[calc(100vh-7rem)] flex justify-center items-center">
                <div className="w-1/4">
                    <h1 className="text-slate-200 font-bold text-4xl mb-4">Trabajos</h1>
                    {this.state.trabajos.map((trabajo, index) => (
                        <Box sx={{ minWidth: 275 }} key={index}>
                            <Card variant="outlined">
                                <CardContent>
                                    <Typography variant="h5" component="div">
                                        {trabajo.nom_trabajo}
                                    </Typography>
                                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                        {trabajo.descripcion_trabajo}
                                    </Typography>
                                    <Typography sx={{ mb: 1.5 }} color="text.secondary">
                                        $ {trabajo.pago}
                                    </Typography>
                                    <Typography variant="body2">
                                        {trabajo.fecha_comienzo}
                                    </Typography>
                                    <Typography variant="body2">
                                        {trabajo.fecha_final}
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    <button className="bg-slate-900 text-slate-300 p-3 rounded block mb-2" onClick={() => {this.props.history.push('/trabajo/edit/'+trabajo._id)}}>Edit</button>
                                    <button className="bg-slate-900 text-slate-300 p-3 rounded block mb-2" onClick={() => {this.props.history.push('/trabajo/delete/'+trabajo._id)}}>Delete</button>
                                </CardActions>
                            </Card>
                        </Box>
                    ))}
                </div>
            </div>
        )
    }
    }

    
