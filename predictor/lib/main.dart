import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// API Configuration - Update this with your API URL
const String apiBaseUrl = 'http://localhost:8000';
const String predictEndpoint = '/predict';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Breast Cancer Survival Predictor',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const PredictionPage(),
    );
  }
}

class PredictionPage extends StatefulWidget {
  const PredictionPage({super.key});

  @override
  State<PredictionPage> createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {
  // Form controllers
  final _formKey = GlobalKey<FormState>();
  final _ageController = TextEditingController();
  final _protein1Controller = TextEditingController();
  final _protein2Controller = TextEditingController();
  final _protein3Controller = TextEditingController();
  final _protein4Controller = TextEditingController();
  final _histologyController = TextEditingController();
  final _surgeryTypeController = TextEditingController();

  // Dropdown values
  String? _selectedGender;
  String? _selectedTumourStage;
  String? _selectedERStatus;
  String? _selectedPRStatus;
  String? _selectedHER2Status;

  // Error message
  String? _errorMessage;
  bool _isLoading = false;

  @override
  void dispose() {
    _ageController.dispose();
    _protein1Controller.dispose();
    _protein2Controller.dispose();
    _protein3Controller.dispose();
    _protein4Controller.dispose();
    _histologyController.dispose();
    _surgeryTypeController.dispose();
    super.dispose();
  }

  Future<void> _predict() async {
    // Reset previous errors
    setState(() {
      _errorMessage = null;
      _isLoading = true;
    });

    // Validate form
    if (!_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = false;
        _errorMessage = 'Please fill in all required fields correctly.';
      });
      return;
    }

    // Check if all dropdowns are selected
    if (_selectedGender == null ||
        _selectedTumourStage == null ||
        _selectedERStatus == null ||
        _selectedPRStatus == null ||
        _selectedHER2Status == null) {
      setState(() {
        _isLoading = false;
        _errorMessage = 'Please select all required dropdown values.';
      });
      return;
    }

    try {
      // Prepare request body
      final requestBody = {
        'Age': int.parse(_ageController.text),
        'Gender': _selectedGender!.toUpperCase(),
        'Protein1': double.parse(_protein1Controller.text),
        'Protein2': double.parse(_protein2Controller.text),
        'Protein3': double.parse(_protein3Controller.text),
        'Protein4': double.parse(_protein4Controller.text),
        'Tumour_Stage': _selectedTumourStage!,
        'Histology': _histologyController.text,
        'ER status': _selectedERStatus!,
        'PR status': _selectedPRStatus!,
        'HER2 status': _selectedHER2Status!,
        'Surgery_type': _surgeryTypeController.text,
      };

      // Make API call
      final url = Uri.parse('$apiBaseUrl$predictEndpoint');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(requestBody),
      );

      // Update UI after receiving response
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _isLoading = false;
          _errorMessage = null;
        });
        // Navigate to results page
        if (mounted) {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ResultsPage(predictionResult: data),
            ),
          );
        }
      } else {
        // Handle API errors
        String errorDetail =
            'An error occurred. Please check your input values.';
        try {
          final errorData = jsonDecode(response.body);
          errorDetail = errorData['detail'] ?? errorDetail;
        } catch (_) {
          // If response body is not valid JSON, use the status code message
          errorDetail =
              'Error ${response.statusCode}: ${response.reasonPhrase ?? "Unknown error"}';
        }
        setState(() {
          _isLoading = false;
          _errorMessage = errorDetail;
        });
      }
    } catch (e) {
      // Handle network errors or JSON parsing errors
      setState(() {
        _isLoading = false;
        _errorMessage =
            'Error connecting to API: ${e.toString()}\n\nPlease ensure the API is running at $apiBaseUrl';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Breast Cancer Survival Predictor'),
        centerTitle: true,
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Age field
              TextFormField(
                controller: _ageController,
                decoration: const InputDecoration(
                  labelText: 'Age *',
                  hintText: 'Enter age (18-100)',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter age';
                  }
                  final age = int.tryParse(value);
                  if (age == null || age < 18 || age > 100) {
                    return 'Age must be between 18 and 100';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Gender dropdown
              DropdownButtonFormField<String>(
                value: _selectedGender,
                decoration: const InputDecoration(
                  labelText: 'Gender *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.wc),
                ),
                items: ['MALE', 'FEMALE'].map((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedGender = newValue;
                  });
                },
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please select gender';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Protein fields
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _protein1Controller,
                      decoration: const InputDecoration(
                        labelText: 'Protein1 *',
                        hintText: '-5.0 to 5.0',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: const TextInputType.numberWithOptions(
                        decimal: true,
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Required';
                        }
                        final protein = double.tryParse(value);
                        if (protein == null ||
                            protein < -5.0 ||
                            protein > 5.0) {
                          return 'Range: -5.0 to 5.0';
                        }
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: TextFormField(
                      controller: _protein2Controller,
                      decoration: const InputDecoration(
                        labelText: 'Protein2 *',
                        hintText: '-5.0 to 5.0',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: const TextInputType.numberWithOptions(
                        decimal: true,
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Required';
                        }
                        final protein = double.tryParse(value);
                        if (protein == null ||
                            protein < -5.0 ||
                            protein > 5.0) {
                          return 'Range: -5.0 to 5.0';
                        }
                        return null;
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _protein3Controller,
                      decoration: const InputDecoration(
                        labelText: 'Protein3 *',
                        hintText: '-5.0 to 5.0',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: const TextInputType.numberWithOptions(
                        decimal: true,
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Required';
                        }
                        final protein = double.tryParse(value);
                        if (protein == null ||
                            protein < -5.0 ||
                            protein > 5.0) {
                          return 'Range: -5.0 to 5.0';
                        }
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: TextFormField(
                      controller: _protein4Controller,
                      decoration: const InputDecoration(
                        labelText: 'Protein4 *',
                        hintText: '-5.0 to 5.0',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: const TextInputType.numberWithOptions(
                        decimal: true,
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Required';
                        }
                        final protein = double.tryParse(value);
                        if (protein == null ||
                            protein < -5.0 ||
                            protein > 5.0) {
                          return 'Range: -5.0 to 5.0';
                        }
                        return null;
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // Tumour Stage dropdown
              DropdownButtonFormField<String>(
                value: _selectedTumourStage,
                decoration: const InputDecoration(
                  labelText: 'Tumour Stage *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.medical_services),
                ),
                items: ['I', 'II', 'III'].map((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedTumourStage = newValue;
                  });
                },
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please select tumour stage';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Histology field
              TextFormField(
                controller: _histologyController,
                decoration: const InputDecoration(
                  labelText: 'Histology *',
                  hintText: 'e.g., Infiltrating Ductal Carcinoma',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.science),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter histology';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Status dropdowns
              Row(
                children: [
                  Expanded(
                    child: DropdownButtonFormField<String>(
                      value: _selectedERStatus,
                      decoration: const InputDecoration(
                        labelText: 'ER Status *',
                        border: OutlineInputBorder(),
                      ),
                      items: ['Positive', 'Negative'].map((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList(),
                      onChanged: (String? newValue) {
                        setState(() {
                          _selectedERStatus = newValue;
                        });
                      },
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Required';
                        }
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: DropdownButtonFormField<String>(
                      value: _selectedPRStatus,
                      decoration: const InputDecoration(
                        labelText: 'PR Status *',
                        border: OutlineInputBorder(),
                      ),
                      items: ['Positive', 'Negative'].map((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList(),
                      onChanged: (String? newValue) {
                        setState(() {
                          _selectedPRStatus = newValue;
                        });
                      },
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Required';
                        }
                        return null;
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // HER2 Status dropdown
              DropdownButtonFormField<String>(
                value: _selectedHER2Status,
                decoration: const InputDecoration(
                  labelText: 'HER2 Status *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.health_and_safety),
                ),
                items: ['Positive', 'Negative'].map((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedHER2Status = newValue;
                  });
                },
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please select HER2 status';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Surgery Type field
              TextFormField(
                controller: _surgeryTypeController,
                decoration: const InputDecoration(
                  labelText: 'Surgery Type *',
                  hintText: 'e.g., Lumpectomy',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.local_hospital),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter surgery type';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),

              // Predict button
              ElevatedButton(
                onPressed: _isLoading ? null : _predict,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: Theme.of(context).colorScheme.primary,
                  foregroundColor: Colors.white,
                ),
                child: _isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor: AlwaysStoppedAnimation<Color>(
                            Colors.white,
                          ),
                        ),
                      )
                    : const Text(
                        'Predict',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
              ),
              const SizedBox(height: 24),

              // Error message display
              if (_errorMessage != null)
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.error_outline, color: Colors.red),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          _errorMessage!,
                          style: const TextStyle(color: Colors.red),
                        ),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

// Results Page
class ResultsPage extends StatelessWidget {
  final Map<String, dynamic> predictionResult;

  const ResultsPage({super.key, required this.predictionResult});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Prediction Results'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Risk Category Card
            Card(
              elevation: 4,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: _getRiskColor(
                    predictionResult['risk_category'] ?? '',
                  ).withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  children: [
                    Text(
                      predictionResult['risk_color'] ?? '🟢',
                      style: const TextStyle(fontSize: 48),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      predictionResult['risk_category'] ?? 'Unknown',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: _getRiskColor(
                          predictionResult['risk_category'] ?? '',
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Prediction Details Card
            Card(
              elevation: 4,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Survival Prediction',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    _buildResultRow(
                      'Predicted Days:',
                      '${predictionResult['predicted_days']?.toStringAsFixed(0) ?? 'N/A'} days',
                    ),
                    const Divider(),
                    _buildResultRow(
                      'Predicted Months:',
                      '${predictionResult['predicted_months']?.toStringAsFixed(1) ?? 'N/A'} months',
                    ),
                    const Divider(),
                    _buildResultRow(
                      'Predicted Years:',
                      '${predictionResult['predicted_years']?.toStringAsFixed(2) ?? 'N/A'} years',
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Recommendation Card
            Card(
              elevation: 4,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          Icons.medical_information,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                        const SizedBox(width: 8),
                        const Text(
                          'Clinical Recommendation',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      predictionResult['recommendation'] ??
                          'No recommendation available',
                      style: const TextStyle(fontSize: 16, height: 1.5),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Back Button
            ElevatedButton.icon(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.arrow_back),
              label: const Text('Back to Form'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: Theme.of(context).colorScheme.primary,
                foregroundColor: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildResultRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          ),
          Text(
            value,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }

  Color _getRiskColor(String riskCategory) {
    switch (riskCategory.toUpperCase()) {
      case 'HIGH RISK':
        return Colors.red;
      case 'ELEVATED RISK':
        return Colors.orange;
      case 'MODERATE RISK':
        return Colors.yellow.shade700;
      case 'LOWER RISK':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }
}
